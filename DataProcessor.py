import TCP
import time
import matplotlib.pyplot as plt


class DataProcessor:

    DEFAULT_MODE = 'close'
    POSITION_MODE = 'position'
    INTENSITY_MODE = 'intensity'
    POWER_MODE = 'power'
    RMS_MODE = 'rms'
    STOP_MODE = 'stop'

    def __init__(self, host, port):
        # Initial Parameters
        self.BPM_DIA = 40
        self.TRIG_TH = 200  # only used for self trigger mode
        self.TRIG_DT = 0
        self.TRIG_DL = 0
        self.EVT_LEN = 1024
        self.EVT_TAIL = 300
        self.BL_LEN = 40

        self.MODE_INT_TRIG = 0x105  # mode reg bit = RUN + Internal trigger + BLR readout
        self.MODE_EXT_TRIG = 0x101  # mode reg bit = RUN + External trigger + BLR readout
        self.MODE_SEL_TRIG = 0x103  # mode reg bit = RUN + Self trigger + BLR readout
        self.MODE_CAL = 0x2105  # mode reg bit = RUN + Self trigger + BLR readout + AFE Cal.

        self.MODE_TEMP = 0x0020  # mode reg bit = Ena temperature reading

        self.A1dB = 0x01  # Analog Front-end board gain setting : 1 dB attenuation
        self.A2dB = 0x02  # Analog Front-end board gain setting : 2 dB attenuation
        self.A4dB = 0x04  # Analog Front-end board gain setting : 4 dB attenuation
        self.A8dB = 0x08  # Analog Front-end board gain setting : 8 dB attenuation
        self.A16dB = 0x10  # Analog Front-end board gain setting : 16 dB attenuation

        self.Gain = self.A1dB + self.A2dB + self.A4dB + self.A8dB + self.A16dB

        self.ChAB = 0
        self.ChCD = 1

        # Data buffers
        self.time_data = []
        self.x_pos_data = []
        self.y_pos_data = []
        self.s_data = []
        self.power_a_data = []
        self.power_b_data = []
        self.power_c_data = []
        self.power_d_data = []
        self.x_rms_data = []
        self.y_rms_data = []

        # ethernet communication
        self.IO = TCP.TCP(host, port)
        self.PACKET_ID = 0x4142504D

        self.current_mode = DataProcessor.DEFAULT_MODE

        plt.ion()

    def init_config(self):
        print self.IO.read_MBver()

        if self.IO.write_reg('BPM:DIA', self.BPM_DIA) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('TRIG:TH', self.TRIG_TH) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('TRIG:DT', self.TRIG_DT) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('TRIG:DL', self.TRIG_DL) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('EVT:LEN', self.EVT_LEN) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('EVT:TAIL', self.EVT_TAIL) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('BL:LEN', self.BL_LEN) is False: exit()
        time.sleep(0.1)

        print 'BPM Diameter (mm) = ', format(self.IO.read_reg('BPM:DIA?'), 'd')
        print 'TRIG:TH =', format(self.IO.read_reg('TRIG:TH?'), 'd')
        print 'TRIG:DT =', format(self.IO.read_reg('TRIG:DT?'), 'd')
        print 'TRIG:DL =', format(self.IO.read_reg('TRIG:DL?'), 'd')
        print 'EVT:LEN =', format(self.IO.read_reg('EVT:LEN?'), 'd')
        print 'EVT:TAIL =', format(self.IO.read_reg('EVT:TAIL?'), 'd')
        print 'BL:LEN =', format(self.IO.read_reg('BL:LEN?'), 'd')

        if self.IO.write_reg('AFE:CTRL', self.Gain) is False: exit()
        time.sleep(0.1)
        if self.IO.write_reg('CR', self.MODE_EXT_TRIG) is False: exit()
        time.sleep(0.1)
        print 'AFE Ctrl Reg = 0x', format(self.IO.read_reg('AFE:CTRL?'), '02x')
        print 'Mode Reg = 0x', format(self.IO.read_reg('CR?'), '02x')

    def view_parameters(self):
        print 'BPM Diameter (mm) = ', format(self.IO.read_reg('BPM:DIA?'), 'd')
        print 'TRIG:TH =', format(self.IO.read_reg('TRIG:TH?'), 'd')
        print 'TRIG:DT =', format(self.IO.read_reg('TRIG:DT?'), 'd')
        print 'TRIG:DL =', format(self.IO.read_reg('TRIG:DL?'), 'd')
        print 'EVT:LEN =', format(self.IO.read_reg('EVT:LEN?'), 'd')
        print 'EVT:TAIL =', format(self.IO.read_reg('EVT:TAIL?'), 'd')
        print 'BL:LEN =', format(self.IO.read_reg('BL:LEN?'), 'd')
        print 'AFE Ctrl Reg = 0x', format(self.IO.read_reg('AFE:CTRL?'), '02x')
        print 'Mode Reg = 0x', format(self.IO.read_reg('CR?'), '02x')

    def view_fifo_occupancy(self):
        print 'Fast FIFO occupancy = ', self.IO.read_ffifo_wd(0)
        print 'Packet FFIFO occupancy = ', self.IO.read_sfifo_wd()

    # using old code for printing and saving waveform data; will need to change this later
    def view_waveform(self):
        samples_to_read = 16 * ((self.EVT_LEN - self.BL_LEN - 4) // 16)
        samples_in_buf = self.IO.read_ffifo_wd(0)
        print "Fast FIFO occupancy: ", samples_in_buf
        if samples_in_buf > samples_to_read:
            waveform = self.IO.read_waveform(self.ChAB, samples_to_read)
            wf_name = raw_input('Press RETURN or Enter waveform file name:')
            wfab_file = wf_name + "ab.wav"
            print "ChA/B waveform file name is : ", wfab_file
            f = open(wfab_file, "w")
            try:
                for i in range(0, samples_to_read - 1):
                    f.write("%d\t%d\n" % (waveform[0][i], waveform[1][i]))
            except TypeError as e:
                print "write file error: "
                print e
            f.close()
            print "ChA waveform saved: max, min value", max(waveform[0]), min(waveform[0])
            print "ChB waveform saved: max, min value", max(waveform[1]), min(waveform[1])
            waveform = self.IO.read_waveform(self.ChCD, samples_to_read)
            wfcd_file = wf_name + "cd.wav"
            print "ChC/D waveform file name is : ", wfcd_file
            f = open(wfcd_file, "w")
            try:
                for i in range(0, samples_to_read - 1):
                    f.write("%d\t%d\n" % (waveform[0][i], waveform[1][i]))
            except TypeError as e:
                print "write file error: "
                print e
            f.close()
            print "ChC waveform saved: max, min value", max(waveform[0]), min(waveform[0])
            print "ChD waveform saved: max, min value", max(waveform[1]), min(waveform[1])

    def set_AFE_gain(self):
        pass

    def set_mode(self, mode):
        self.current_mode = mode

    def get_mode(self):
        return self.current_mode

    def setup_plot(self):
        # clear the figure
        fig = plt.gcf()
        plt.clf()
        if self.current_mode == DataProcessor.INTENSITY_MODE:
            ax = fig.add_subplot(111)
            ax.set_ylabel('S Intensity')
            ax.set_xlabel('Time (s)')
            ax.set_gid(self.current_mode)
            ax.plot(self.time_data, self.s_data)
        else:
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)
            if self.current_mode == DataProcessor.POSITION_MODE:
                ax1.set_ylabel('X position (um)')
                ax2.set_ylabel('Y position (um)')
                ax1.plot(self.time_data, self.x_pos_data)
                ax2.plot(self.time_data, self.y_pos_data)
            elif self.current_mode == DataProcessor.POWER_MODE:
                ax1.set_ylabel('Power AB')
                ax2.set_ylabel('Power CD')
                ax1.plot(self.time_data, self.power_a_data, 'b-', label='A')
                ax1.plot(self.time_data, self.power_b_data, 'r-', label='B')
                ax2.plot(self.time_data, self.power_c_data, 'b-', label='C')
                ax2.plot(self.time_data, self.power_d_data, 'r-', label='D')
                ax1.legend()
                ax2.legend()
            elif self.current_mode == DataProcessor.RMS_MODE:
                ax1.set_ylabel('X res. rms (um)')
                ax2.set_ylabel('Y res. rms (um)')
                ax1.plot(self.time_data, self.x_rms_data)
                ax2.plot(self.time_data, self.y_rms_data)

            # gid is only set for the first axes (it would be the same for the second)
            ax1.set_gid(self.current_mode)
            ax2.set_xlabel('Time(s)')

    def update_plot(self):
        if self.current_mode == DataProcessor.INTENSITY_MODE:
            ax1, = plt.gcf().get_axes()
            ax1.get_lines()[0].set_data(self.time_data, self.s_data)
        else:
            ax1, ax2 = plt.gcf().get_axes()
            if self.current_mode == DataProcessor.POSITION_MODE:
                ax1.get_lines()[0].set_data(self.time_data, self.x_pos_data)
                ax2.get_lines()[0].set_data(self.time_data, self.y_pos_data)
            elif self.current_mode == DataProcessor.POWER_MODE:
                ax1.get_lines()[0].set_data(self.time_data, self.power_a_data)
                ax1.get_lines()[1].set_data(self.time_data, self.power_b_data)
                ax2.get_lines()[0].set_data(self.time_data, self.power_c_data)
                ax2.get_lines()[1].set_data(self.time_data, self.power_d_data)
            elif self.current_mode == DataProcessor.RMS_MODE:
                ax1.get_lines()[0].set_data(self.time_data, self.x_rms_data)
                ax2.get_lines()[0].set_data(self.time_data, self.y_rms_data)

        ax1.relim()
        ax1.autoscale_view()

        # if ax2 is defined
        if 'ax2' in locals():
            ax2.relim()
            ax2.autoscale_view()

        plt.pause(0.1)

    # Looks at the slow fifo occupancy; if it is greater than 16, then a packet is read from the slow fifo
    # and the appropriate data buffers (x, y, etc.) are updated
    def read_data(self, current_time):
        samples_in_sfifo = self.IO.read_sfifo_wd()
        if samples_in_sfifo > 16:
            packet = self.IO.read_buffer('SFIFO:DATA?')  # read one packet from FPGA buffer
            if packet[0] != self.PACKET_ID:
                raise TypeError('Packet ID error!')

            # extract new data from packet
            x = TCP.s16(packet[3] >> 16)
            y = TCP.s16(packet[3] & 0xFFFF)
            s = TCP.s16(packet[4] >> 16)
            PA = packet[5]
            PB = packet[6]
            PC = packet[7]
            PD = packet[8]

            # add new data to old data
            self.time_data.append(current_time + 1)
            self.x_pos_data.append(x)
            self.y_pos_data.append(y)
            self.s_data.append(s)
            self.power_a_data.append(PA)
            self.power_b_data.append(PB)
            self.power_c_data.append(PC)
            self.power_d_data.append(PD)

            x_rms = int(TCP.rms(self.x_pos_data))
            y_rms = int(TCP.rms(self.y_pos_data))
            self.x_rms_data.append(x_rms)
            self.y_rms_data.append(y_rms)

    def clear_data(self):
        del self.time_data[:]
        del self.x_pos_data[:]
        del self.y_pos_data[:]
        del self.s_data[:]
        del self.power_a_data[:]
        del self.power_b_data[:]
        del self.power_c_data[:]
        del self.power_d_data[:]
        del self.x_rms_data[:]
        del self.y_rms_data[:]

    def close_windows(self):
        plt.close()

    def shutdown(self):
        self.IO.destroy()
        plt.ioff()
