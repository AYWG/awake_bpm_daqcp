import TCP
import time
import sys
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import Modes
import Plots
import threading


class DataProcessor:
    def __init__(self, host, port):
        # Initial Parameters
        self.bpm_dia = 40
        self.trig_th = 200  # only used for self trigger mode
        self.trig_dt = 0
        self.trig_dl = 0
        self.evt_len = 1024
        self.evt_tail = 300
        self.bl_len = 40

        self.ch_gain_a = 1.0
        self.ch_gain_b = 1.0
        self.ch_gain_c = 1.0
        self.ch_gain_d = 1.0

        self.cal_gain_a = 1.0
        self.cal_gain_b = 1.0
        self.cal_gain_c = 1.0
        self.cal_gain_d = 1.0

        # self.MODE_INT_TRIG = 0x105  # mode reg bit = RUN + Internal trigger + BLR readout       0000 0001 0000 0101
        # self.MODE_EXT_TRIG = 0x101  # mode reg bit = RUN + External trigger + BLR readout       0000 0001 0000 0001
        # self.MODE_SEL_TRIG = 0x103  # mode reg bit = RUN + Self trigger + BLR readout           0000 0001 0000 0011
        # self.MODE_CAL = 0x2105  # mode reg bit = RUN + Self trigger + BLR readout + AFE Cal.    0010 0001 0000 0101

        # self.MODE_TEMP = 0x0020  # mode reg bit = Ena temperature reading                       0000 0000 0010 0000

        self.mode = 0x101 # mode reg bit = RUN + External trigger + BLR readout

        self.gain = 0x1F # 31 dB attenuation

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

        self.lock = threading.Lock()

        # Initial mode of operation is PAUSED
        self.op_mode = Modes.PAUSED

        # There is no plot at the beginning
        self.plot = Plots.NONE

        plt.ion()

    def init_config(self):
        with self.lock:
            print self.IO.read_MBver()

            if self.IO.write_reg('BPM:DIA', self.bpm_dia) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('TRIG:TH', self.trig_th) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('TRIG:DT', self.trig_dt) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('TRIG:DL', self.trig_dl) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('EVT:LEN', self.evt_len) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('EVT:TAIL', self.evt_tail) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('BL:LEN', self.bl_len) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('AFE:CTRL', self.gain) is False: sys.exit()
            time.sleep(0.1)
            if self.IO.write_reg('CR', self.mode) is False: sys.exit()
            time.sleep(0.1)

    def get_mode(self):
        with self.lock:
            return self.IO.read_reg('CR?')

    def set_mode(self, mode):
        with self.lock:
            if self.IO.write_reg('CR', mode) is False: sys.exit()
            time.sleep(0.1)

    def get_afe_gain(self):
        with self.lock:
            return self.IO.read_reg('AFE:CTRL?')

    def set_afe_gain(self, gain):
        with self.lock:
            if self.IO.write_reg('AFE:CTRL', gain) is False: sys.exit()
            time.sleep(0.1)

    def get_bl_len(self):
        with self.lock:
            return self.IO.read_reg('BL:LEN?')

    def set_bl_len(self, bl_len):
        with self.lock:
            if self.IO.write_reg('BL:LEN', bl_len) is False: sys.exit()
            time.sleep(0.1)

    def get_evt_len(self):
        with self.lock:
            return self.IO.read_reg('EVT:LEN?')

    def set_evt_len(self, evt_len):
        with self.lock:
            if self.IO.write_reg('EVT:LEN', evt_len) is False: sys.exit()
            time.sleep(0.1)

    def get_evt_tail(self):
        with self.lock:
            return self.IO.read_reg('EVT:TAIL?')

    def set_evt_tail(self, evt_tail):
        with self.lock:
            if self.IO.write_reg('EVT:TAIL', evt_tail) is False: sys.exit()
            time.sleep(0.1)

    def get_trig_th(self):
        with self.lock:
            return self.IO.read_reg('TRIG:TH?')

    def set_trig_th(self, trig_th):
        with self.lock:
            if self.IO.write_reg('TRIG:TH', trig_th) is False: sys.exit()
            time.sleep(0.1)

    def get_trig_dt(self):
        with self.lock:
            return self.IO.read_reg('TRIG:DT?')

    def set_trig_dt(self, trig_dt):
        with self.lock:
            if self.IO.write_reg('TRIG:DT', trig_dt) is False: sys.exit()
            time.sleep(0.1)

    def get_trig_dl(self):
        with self.lock:
            return self.IO.read_reg('TRIG:DL?')

    def set_trig_dl(self, trig_dl):
        with self.lock:
            if self.IO.write_reg('TRIG:DL', trig_dl) is False: sys.exit()
            time.sleep(0.1)

    def get_bpm_dia(self):
        with self.lock:
            return self.IO.read_reg('BPM:DIA?')

    def set_bpm_dia(self, bpm_dia):
        with self.lock:
            if self.IO.write_reg('BPM:DIA', bpm_dia) is False: sys.exit()
            time.sleep(0.1)

    def get_cal_gain_a(self):
        with self.lock:
            return self.IO.read_reg('CAL:GAIN:A?')

    def set_cal_gain_a(self, cal_gain_a):
        with self.lock:
            if self.IO.write_reg('CAL:GAIN:A', cal_gain_a) is False: sys.exit()
            time.sleep(0.1)

    def get_cal_gain_b(self):
        with self.lock:
            return self.IO.read_reg('CAL:GAIN:B?')

    def set_cal_gain_b(self, cal_gain_b):
        with self.lock:
            if self.IO.write_reg('CAL:GAIN:B', cal_gain_b) is False: sys.exit()
            time.sleep(0.1)

    def get_cal_gain_c(self):
        with self.lock:
            return self.IO.read_reg('CAL:GAIN:C?')

    def set_cal_gain_c(self, cal_gain_c):
        with self.lock:
            if self.IO.write_reg('CAL:GAIN:C', cal_gain_c) is False: sys.exit()
            time.sleep(0.1)

    def get_cal_gain_d(self):
        with self.lock:
            return self.IO.read_reg('CAL:GAIN:D?')

    def set_cal_gain_d(self, cal_gain_d):
        with self.lock:
            if self.IO.write_reg('CAL:GAIN:D', cal_gain_d) is False: sys.exit()
            time.sleep(0.1)

    def get_ch_gain_a(self):
        with self.lock:
            return self.IO.read_reg('CH:GAIN:A?')

    def set_ch_gain_a(self, ch_gain_a):
        with self.lock:
            if self.IO.write_reg('CH:GAIN:A', ch_gain_a) is False: sys.exit()
            time.sleep(0.1)

    def get_ch_gain_b(self):
        with self.lock:
            return self.IO.read_reg('CH:GAIN:B?')

    def set_ch_gain_b(self, ch_gain_b):
        with self.lock:
            if self.IO.write_reg('CH:GAIN:B', ch_gain_b) is False: sys.exit()
            time.sleep(0.1)

    def get_ch_gain_c(self):
        with self.lock:
            return self.IO.read_reg('CH:GAIN:C?')

    def set_ch_gain_c(self, ch_gain_c):
        with self.lock:
            if self.IO.write_reg('CH:GAIN:C', ch_gain_c) is False: sys.exit()
            time.sleep(0.1)

    def get_ch_gain_d(self):
        with self.lock:
            return self.IO.read_reg('CH:GAIN:D?')

    def set_ch_gain_d(self, ch_gain_d):
        with self.lock:
            if self.IO.write_reg('CH:GAIN:D', ch_gain_d) is False: sys.exit()
            time.sleep(0.1)

    def wr_flash_buf(self):
        with self.lock:
            if self.IO.write_reg('FPGA:TO:FLASHBUF', 0) is False: sys.exit()  # the 0 is arbitrary
            time.sleep(0.1)

    def rd_flash(self):
        with self.lock:
            if self.IO.write_reg('FLASH:READ', 0) is False: sys.exit()  # the 0 is arbitrary
            time.sleep(0.1)
            if self.IO.write_reg('FLASHBUF:TO:FPGA', 0) is False: sys.exit()  # the 0 is arbitrary
            time.sleep(0.1)

    def wr_flash(self):
        with self.lock:
            if self.IO.write_reg('FLASH:WRIT', 0) is False: sys.exit()  # the 0 is arbitrary
            time.sleep(0.1)

    def get_mac_address(self, index):
        with self.lock:
            return self.IO.read_reg('FL:BUF:MAC:' + str(index) + '?')

    def set_mac_address(self, index, value):
        with self.lock:
            if self.IO.write_reg('FL:BUF:MAC:' + str(index), value) is False: sys.exit()
            time.sleep(0.1)

    def get_ip_address(self, index):
        with self.lock:
            return self.IO.read_reg('FL:BUF:IP:' + str(index) + '?')

    def set_ip_address(self, index, value):
        with self.lock:
            if self.IO.write_reg('FL:BUF:IP:' + str(index), value) is False: sys.exit()
            time.sleep(0.1)

    def float_to_int(self, f):
        """
        Returns the integer representation of the IEEE 754 format of the given python
        floating point value.
        For example, 1.0 returns 1065353216
        :param f:
        :return:
        """
        import struct
        return struct.unpack('<i', struct.pack('<f', f))[0]

    def int_to_float(self, i):
        """
        Returns the python floating point representation of the IEEE 754 format integer
        :param i:
        :return:
        """
        import struct
        return struct.unpack('<f', struct.pack('<i', i))[0]

    # -------------- Methods for managing the plot

    def get_average(self, data_buffer):
        """
        :param data_buffer: a list of data (e.g. x_pos_data)
        :return: rounded average of all elements of data_buffer
        """
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
        """
        Builds the given plot in a new window, or changes the current plot to the given plot if the window
        is already open.
        :param plot: The plot to setup.
        """
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
                    ax1.text(1.02, 0.2, 'X Avg:', transform=ax1.transAxes, fontsize=8)
                    self.x_pos_avg = ax1.text(1.1, 0.2, str(self.get_average(self.x_pos_data)),
                                                                        transform=ax1.transAxes, fontsize=8)

                    ax1.text(1.02, 0.1, 'Y Avg:', transform=ax1.transAxes, fontsize=8)
                    self.y_pos_avg = ax1.text(1.1, 0.1, str(self.get_average(self.y_pos_data)),
                                              transform=ax1.transAxes, fontsize=8)
                elif plot == Plots.POWER:
                    ax1.set_title('Power')
                    ax1.set_ylabel('Power AB')
                    ax2.set_ylabel('Power CD')
                    ax1.plot(self.time_data, self.power_a_data, 'b-', label='A')
                    ax1.plot(self.time_data, self.power_b_data, 'r-', label='B')
                    ax2.plot(self.time_data, self.power_c_data, 'b-', label='C')
                    ax2.plot(self.time_data, self.power_d_data, 'r-', label='D')
                    # Display running average
                    ax1.text(1.02, 0.2, 'A Avg:', transform=ax1.transAxes, fontsize=8)
                    self.power_a_avg = ax1.text(1.1, 0.2, str(self.get_average(self.power_a_data)),
                                                transform=ax1.transAxes, fontsize=8)
                    ax1.text(1.02, 0.1, 'B Avg:', transform=ax1.transAxes, fontsize=8)
                    self.power_b_avg = ax1.text(1.1, 0.1, str(self.get_average(self.power_b_data)),
                                                transform=ax1.transAxes, fontsize=8)
                    ax2.text(1.02, 0.2, 'C Avg:', transform=ax2.transAxes, fontsize=8)
                    self.power_c_avg = ax2.text(1.1, 0.2, str(self.get_average(self.power_c_data)),
                                                transform=ax2.transAxes, fontsize=8)
                    ax2.text(1.02, 0.1, 'D Avg:', transform=ax2.transAxes, fontsize=8)
                    self.power_d_avg = ax2.text(1.1, 0.1, str(self.get_average(self.power_d_data)),
                                                transform=ax2.transAxes, fontsize=8)

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
            fig.canvas.start_event_loop(0.5)

    @staticmethod
    def enable_plot_interaction():
        """
        This method allows the user to interact with a plot when data is not being collected (i.e. op_mode is PAUSED
        or op_mode is RUNNING but Run is not enabled in the GUI)
        """
        if plt.get_fignums():
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
        """
        Checks if there is enough data in the fast fifo for reading
        :return: True | False
        """
        with self.lock:
            self.samples_to_read = 16 * ((self.evt_len - self.bl_len - 4) // 16)
            samples_in_buf = self.IO.read_ffifo_wd(0)
            return samples_in_buf > self.samples_to_read

    def is_new_data_rdy(self):
        """
        Determines if a a new packet of data is ready to be read from the slow fifo in the FPGA
        :return: True | False
        """
        with self.lock:
            samples_in_sfifo = self.IO.read_sfifo_wd()
            return samples_in_sfifo > 16

    def read_data(self):
        """
        Read a packet of data from the slow fifo in the FPGA and update the appropriate data buffers (x, y, etc.)
        """
        with self.lock:
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
        with self.lock:
            waveform_AB = self.IO.read_waveform(self.ChAB, self.samples_to_read)
            waveform_CD = self.IO.read_waveform(self.ChCD, self.samples_to_read)
            # False if waveform not successfully read
            if waveform_AB:
                self.raw_adc_a_data = waveform_AB[0]
                self.raw_adc_b_data = waveform_AB[1]
            if waveform_CD:
                self.raw_adc_c_data = waveform_CD[0]
                self.raw_adc_d_data = waveform_CD[1]

    def clear_data(self):
        """
        Resets all data buffers and sets the current time to 0
        """
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
