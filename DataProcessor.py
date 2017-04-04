import TCP
import time
import sys
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import Modes
import Plots


class DataProcessor:
    def __init__(self, host, port):
        # Initial Parameters
        self.BPM_DIA = 40
        self.TRIG_TH = 200  # only used for self trigger mode
        self.TRIG_DT = 0
        self.TRIG_DL = 0
        self.EVT_LEN = 1024
        self.EVT_TAIL = 300
        self.BL_LEN = 40

        self.ch_gain_a = 1.0
        self.ch_gain_b = 1.0
        self.ch_gain_c = 1.0
        self.ch_gain_d = 1.0

        self.cal_gain_a = 1.0
        self.cal_gain_b = 1.0
        self.cal_gain_c = 1.0
        self.cal_gain_d = 1.0

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
        self.current_time = 0
        self.raw_adc_a_data = []
        self.raw_adc_b_data = []
        self.raw_adc_c_data = []
        self.raw_adc_d_data = []
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

        self.power_a_avg = ''
        self.power_b_avg = ''
        self.power_c_avg = ''
        self.power_d_avg = ''

        self.x_pos_avg = ''
        self.y_pos_avg = ''

        self.samples_to_read = 0

        # ethernet communication
        self.IO = TCP.TCP(host, port)
        self.PACKET_ID = 0x4142504D

        # Initial mode of operation is PAUSED
        self.op_mode = Modes.PAUSED

        # Initial plot is NONE
        self.plot = Plots.NONE

        plt.ion()

    def init_config(self):
        print self.IO.read_MBver()

        if self.IO.write_reg('BPM:DIA', self.BPM_DIA) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('TRIG:TH', self.TRIG_TH) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('TRIG:DT', self.TRIG_DT) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('TRIG:DL', self.TRIG_DL) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('EVT:LEN', self.EVT_LEN) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('EVT:TAIL', self.EVT_TAIL) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('BL:LEN', self.BL_LEN) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('AFE:CTRL', self.Gain) is False: sys.exit()
        time.sleep(0.1)
        if self.IO.write_reg('CR', self.MODE_EXT_TRIG) is False: sys.exit()
        time.sleep(0.1)

    # using old code for printing and saving waveform data; will need to change this later
    def view_waveform(self):
        samples_to_read = 16 * ((self.EVT_LEN - self.BL_LEN - 4) // 16)
        samples_in_buf = self.IO.read_ffifo_wd(0)
        print "Fast FIFO occupancy: ", samples_in_buf
        # condition for reading waveform data
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
            # wfcd_file = wf_name + "cd.wav"
            # print "ChC/D waveform file name is : ", wfcd_file
            # f = open(wfcd_file, "w")
            # try:
            #     for i in range(0, samples_to_read - 1):
            #         f.write("%d\t%d\n" % (waveform[0][i], waveform[1][i]))

    def set_afe_gain(self, gain):
        self.Gain = gain
        if self.IO.write_reg('AFE:CTRL', gain) is False: sys.exit()
        time.sleep(0.1)

    def set_bl_len(self, bl_len):
        self.BL_LEN = bl_len
        if self.IO.write_reg('BL:LEN', bl_len) is False: sys.exit()
        time.sleep(0.1)

    def set_evt_len(self, evt_len):
        self.EVT_LEN = evt_len
        if self.IO.write_reg('EVT:LEN', evt_len) is False: sys.exit()
        time.sleep(0.1)

    def set_evt_tail(self, evt_tail):
        self.EVT_TAIL = evt_tail
        if self.IO.write_reg('EVT:TAIL', evt_tail) is False: sys.exit()
        time.sleep(0.1)

    def set_trig_th(self, trig_th):
        self.TRIG_TH = trig_th
        if self.IO.write_reg('TRIG:TH', trig_th) is False: sys.exit()
        time.sleep(0.1)

    def set_trig_dt(self, trig_dt):
        self.TRIG_DT = trig_dt
        if self.IO.write_reg('TRIG:DT', trig_dt) is False: sys.exit()
        time.sleep(0.1)

    def set_trigger_mode(self, trigger_mode):
        if trigger_mode == 0:
            if self.IO.write_reg('CR', self.MODE_EXT_TRIG) is False: sys.exit()
        elif trigger_mode == 1:
            if self.IO.write_reg('CR', self.MODE_INT_TRIG) is False: sys.exit()
        elif trigger_mode == 2:
            if self.IO.write_reg('CR', self.MODE_SEL_TRIG) is False: sys.exit()
        elif trigger_mode == 3:
            if self.IO.write_reg('CR', self.MODE_CAL) is False: sys.exit()

    def set_trig_dl(self, trig_dl):
        self.TRIG_DL = trig_dl
        if self.IO.write_reg('TRIG:DL', trig_dl) is False: sys.exit()
        time.sleep(0.1)

    def set_bpm_dia(self, bpm_dia):
        self.BPM_DIA = bpm_dia
        if self.IO.write_reg('BPM:DIA', bpm_dia) is False: sys.exit()
        time.sleep(0.1)

    def set_cal_gain_a(self, cal_gain_a):
        self.cal_gain_a = cal_gain_a
        if self.IO.write_reg('CAL:GAIN:A', cal_gain_a) is False: sys.exit()
        time.sleep(0.1)

    def set_cal_gain_b(self, cal_gain_b):
        self.cal_gain_b = cal_gain_b
        if self.IO.write_reg('CAL:GAIN:B', cal_gain_b) is False: sys.exit()
        time.sleep(0.1)

    def set_cal_gain_c(self, cal_gain_c):
        self.cal_gain_c = cal_gain_c
        if self.IO.write_reg('CAL:GAIN:C', cal_gain_c) is False: sys.exit()
        time.sleep(0.1)

    def set_cal_gain_d(self, cal_gain_d):
        self.cal_gain_d = cal_gain_d
        if self.IO.write_reg('CAL:GAIN:D', cal_gain_d) is False: sys.exit()
        time.sleep(0.1)

    def set_ch_gain_a(self, ch_gain_a):
        self.ch_gain_a = ch_gain_a
        if self.IO.write_reg('CH:GAIN:A', ch_gain_a) is False: sys.exit()
        time.sleep(0.1)

    def set_ch_gain_b(self, ch_gain_b):
        self.ch_gain_b = ch_gain_b
        if self.IO.write_reg('CH:GAIN:B', ch_gain_b) is False: sys.exit()
        time.sleep(0.1)

    def set_ch_gain_c(self, ch_gain_c):
        self.ch_gain_c = ch_gain_c
        if self.IO.write_reg('CH:GAIN:C', ch_gain_c) is False: sys.exit()
        time.sleep(0.1)

    def set_ch_gain_d(self, ch_gain_d):
        self.ch_gain_d = ch_gain_d
        if self.IO.write_reg('CH:GAIN:D', ch_gain_d) is False: sys.exit()
        time.sleep(0.1)

    def wr_flash_buf(self):
        if self.IO.write_reg('FPGA:TO:FLASHBUF', 0) is False: sys.exit()  # the 0 is arbitrary
        time.sleep(0.1)

    # For testing
    def get_trig_th(self):
        return self.IO.read_reg('TRIG:TH?')

    # Returns the hexadecimal representation of the IEEE 754 format of the given python floating point value
    # e.g. 1.0 returns 0x3f800000
    def float_to_hex(self, f):
        import struct
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    # -------------- Methods for managing the plot

    def get_average(self, data_buffer):
        # Empty
        if not data_buffer:
            return float('NaN')
        else:
            sum = 0.0
            for i in range(0, len(data_buffer)):
                sum += data_buffer[i]

            # rounded average
            return round(sum / len(data_buffer))

    def set_op_mode(self, op_mode):
        self.op_mode = op_mode

    def get_op_mode(self):
        return self.op_mode

    def set_plot(self, plot):
        self.plot = plot

    def get_plot(self):
        return self.plot

    def setup_plot(self, plot):
        # only take action if the current plot is not the same as the provided plot
        if self.get_plot() != plot:
            self.set_plot(plot)

            # clear the figure
            fig = plt.gcf()
            plt.clf()

            if plot == Plots.INTENSITY:
                ax = fig.add_subplot(111)
                ax.set_title('Intensity')
                # labelpad is for adding space between y axis label and tick labels
                ax.set_ylabel('S Intensity', labelpad=10)
                ax.set_xlabel('Time (s)')
                # ax.tick_params(axis='both', which='major', pad=15)
                ax.plot(self.time_data, self.s_data)
            else:
                ax1 = fig.add_subplot(211)
                ax2 = fig.add_subplot(212)
                # Disables scientific notation for tick labels
                # ax1.get_yaxis().get_major_formatter().set_scientific(False)
                # ax2.get_yaxis().get_major_formatter().set_scientific(False)
                if plot == Plots.WAVEFORM:
                    ax1.set_title('ADC 16 bit data RAW or after BLR/Gain Cor.')
                    ax1.set_ylabel('ADC output 16 bit')
                    ax2.set_ylabel('ADC output 16 bit')
                    ax1.plot(range(len(self.raw_adc_a_data)), self.raw_adc_a_data, 'b-', label='A')
                    ax1.plot(range(len(self.raw_adc_b_data)), self.raw_adc_b_data, 'r-', label='B')
                    ax2.plot(range(len(self.raw_adc_c_data)), self.raw_adc_c_data, 'b-', label='C')
                    ax2.plot(range(len(self.raw_adc_d_data)), self.raw_adc_d_data, 'r-', label='D')

                elif plot == Plots.POSITION:
                    ax1.set_title('Position and Res. RMS')
                    ax1.set_ylabel('X/Y position (um)')
                    ax2.set_ylabel('X/Y res. rms (um)')
                    ax1.plot(self.time_data, self.x_pos_data, 'b-', label='X pos')
                    ax1.plot(self.time_data, self.y_pos_data, 'r-', label='Y pos')
                    ax2.plot(self.time_data, self.x_rms_data, 'b-', label='X rms')
                    ax2.plot(self.time_data, self.y_rms_data, 'r-', label='Y rms')
                    # Display running average
                    self.x_pos_avg = ax1.text(0.05, 0.90, str(self.get_average(self.x_pos_data)),
                                              transform=ax1.transAxes, fontsize=10)
                    self.y_pos_avg = ax1.text(0.05, 0.80, str(self.get_average(self.y_pos_data)),
                                              transform=ax1.transAxes, fontsize=10)
                elif plot == Plots.POWER:
                    ax1.set_title('Power')
                    ax1.set_ylabel('Power AB')
                    ax2.set_ylabel('Power CD')
                    ax1.plot(self.time_data, self.power_a_data, 'b-', label='A')
                    ax1.plot(self.time_data, self.power_b_data, 'r-', label='B')
                    ax2.plot(self.time_data, self.power_c_data, 'b-', label='C')
                    ax2.plot(self.time_data, self.power_d_data, 'r-', label='D')
                    # Display running average
                    self.power_a_avg = ax1.text(0.05, 0.90, str(self.get_average(self.power_a_data)),
                                                transform=ax1.transAxes, fontsize=10)
                    self.power_b_avg = ax1.text(0.05, 0.80, str(self.get_average(self.power_b_data)),
                                                transform=ax1.transAxes, fontsize=10)
                    self.power_c_avg = ax2.text(0.05, 0.90, str(self.get_average(self.power_c_data)),
                                                transform=ax2.transAxes, fontsize=10)
                    self.power_d_avg = ax2.text(0.05, 0.80, str(self.get_average(self.power_d_data)),
                                                transform=ax2.transAxes, fontsize=10)

                # Add a legend to distinguish plots on the same axes
                box1 = ax1.get_position()
                box2 = ax2.get_position()
                # Shrink current axis's width by 10% on the right
                ax1.set_position([box1.x0, box1.y0, box1.width * 0.9, box1.height])
                ax2.set_position([box2.x0, box2.y0, box2.width * 0.9, box2.height])
                ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                # Both axes share the same x label, so we only need one
                ax2.set_xlabel('Time(s)')

            fig.canvas.mpl_connect('close_event', self.close_windows)
            fig.canvas.draw()
            # plt.show(block=False)
            fig.canvas.start_event_loop(5)

    @staticmethod
    def enable_plot_interaction():
        plt.gcf().canvas.start_event_loop(0.1)

    # Updates the active plot, adjusting the appropriate axis based on the data collected so far
    def update_plot(self):
        # Only take action if there's an active plot
        if self.get_plot() != Plots.NONE:
            if self.get_plot() == Plots.INTENSITY:
                ax1, = plt.gcf().get_axes()
                ax1.get_lines()[0].set_data(self.time_data, self.s_data)
            else:
                ax1, ax2 = plt.gcf().get_axes()
                # if self.get_plot() == Plots.WAVEFORM:
                #     ax1.get_lines()[0].set_data(range(len(self.raw_adc_a_data)), self.raw_adc_a_data)
                #     ax1.get_lines()[1].set_data(range(len(self.raw_adc_b_data)), self.raw_adc_b_data)
                #     ax2.get_lines()[0].set_data(range(len(self.raw_adc_c_data)), self.raw_adc_c_data)
                #     ax2.get_lines()[1].set_data(range(len(self.raw_adc_d_data)), self.raw_adc_d_data)
                if self.get_plot() == Plots.POSITION:
                    ax1.get_lines()[0].set_data(self.time_data, self.x_pos_data)
                    ax1.get_lines()[1].set_data(self.time_data, self.y_pos_data)
                    ax2.get_lines()[0].set_data(self.time_data, self.x_rms_data)
                    ax2.get_lines()[1].set_data(self.time_data, self.y_rms_data)
                    self.x_pos_avg.set_text(str(self.get_average(self.x_pos_data)))
                    self.y_pos_avg.set_text(str(self.get_average(self.y_pos_data)))
                elif self.get_plot() == Plots.POWER:
                    ax1.get_lines()[0].set_data(self.time_data, self.power_a_data)
                    ax1.get_lines()[1].set_data(self.time_data, self.power_b_data)
                    ax2.get_lines()[0].set_data(self.time_data, self.power_c_data)
                    ax2.get_lines()[1].set_data(self.time_data, self.power_d_data)
                    self.power_a_avg.set_text(str(self.get_average(self.power_a_data)))
                    self.power_b_avg.set_text(str(self.get_average(self.power_b_data)))
                    self.power_c_avg.set_text(str(self.get_average(self.power_c_data)))
                    self.power_d_avg.set_text(str(self.get_average(self.power_d_data)))

                ax2.relim()
                ax2.autoscale_view()

            ax1.relim()
            ax1.autoscale_view()

            plt.gcf().canvas.draw()
            # plt.show(block=False)
            plt.gcf().canvas.start_event_loop(0.5)

    def update_waveform(self):
        if self.get_plot() == Plots.WAVEFORM:
            ax1, ax2 = plt.gcf().get_axes()
            ax1.get_lines()[0].set_data(range(len(self.raw_adc_a_data)), self.raw_adc_a_data)
            ax1.get_lines()[1].set_data(range(len(self.raw_adc_b_data)), self.raw_adc_b_data)
            ax2.get_lines()[0].set_data(range(len(self.raw_adc_c_data)), self.raw_adc_c_data)
            ax2.get_lines()[1].set_data(range(len(self.raw_adc_d_data)), self.raw_adc_d_data)
            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            plt.gcf().canvas.draw()
            plt.gcf().canvas.start_event_loop(0.1)

    def is_waveform_rdy(self):
        self.samples_to_read = 16 * ((self.EVT_LEN - self.BL_LEN - 4) // 16)
        samples_in_buf = self.IO.read_ffifo_wd(0)
        return samples_in_buf > self.samples_to_read

    # Determines if a a new packet of data is ready to be read from the slow fifo in the FPGA.
    def is_new_data_rdy(self):
        samples_in_sfifo = self.IO.read_sfifo_wd()
        return samples_in_sfifo > 16

    # Read a packet of data from the slow fifo in the FPGA and update the appropriate data buffers (x, y, etc.)
    def read_data(self):
        packet = self.IO.read_buffer('SFIFO:DATA?')  # read one packet from FPGA buffer
        if packet[0] != self.PACKET_ID:
            raise TypeError('Packet ID error!')

        self.current_time += 1
        # extract new data from packet
        x = TCP.s16(packet[3] >> 16)
        y = TCP.s16(packet[3] & 0xFFFF)
        s = TCP.s16(packet[4] >> 16)
        PA = packet[5]
        PB = packet[6]
        PC = packet[7]
        PD = packet[8]

        # add new data to old data
        self.time_data.append(self.current_time)
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

    def read_waveform(self):
        waveform_AB = self.IO.read_waveform(self.ChAB, self.samples_to_read)
        waveform_CD = self.IO.read_waveform(self.ChCD, self.samples_to_read)
        self.raw_adc_a_data = waveform_AB[0]
        self.raw_adc_b_data = waveform_AB[1]
        self.raw_adc_c_data = waveform_CD[0]
        self.raw_adc_d_data = waveform_CD[1]

    # Resets all data buffers and sets the current time to 0
    def clear_data(self):
        self.current_time = 0
        del self.raw_adc_a_data[:]
        del self.raw_adc_b_data[:]
        del self.raw_adc_c_data[:]
        del self.raw_adc_d_data[:]
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

    # Closes control window and any active plots
    def close_windows(self):
        self.set_plot(Plots.NONE)
        plt.close('all')

    def shutdown(self):
        self.close_windows()
        self.clear_data()
        self.IO.destroy()
        plt.ioff()
