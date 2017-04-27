import sys
import time
import matplotlib
import TCP

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from Constants import Plots, Modes
import threading
import warnings

warnings.filterwarnings("ignore")  # For suppressing a deprecation warning


class DataProcessor:
    """
    Main class responsible for
    - communicating with the BPM via ethernet
    - managing the plots
    """

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

        self.mode = 0x101  # mode reg bit = RUN + External trigger + BLR readout

        self.gain = 0x1F  # 31 dB attenuation

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

        # Averages are displayed in the plots as strings
        self.power_a_avg = ''
        self.power_b_avg = ''
        self.power_c_avg = ''
        self.power_d_avg = ''

        self.x_pos_avg = ''
        self.y_pos_avg = ''

        self.samples_to_read = 0
        self.evt_num = 0
        self.ffifo_ab_words = 0
        self.ffifo_cd_words = 0
        self.sfifo_words = 0

        # ethernet communication
        self.IO = TCP.TCP(host, port)
        self.PACKET_ID = 0x4142504D

        # We need a lock for the ethernet communication
        self.eth_lock = threading.Lock()

        # We need a lock for managing collected data
        self.data_lock = threading.Lock()

        # We need a lock for the GUI
        self.gui_lock = threading.Lock()

        # Initial mode of operation is PAUSED
        self.op_mode = Modes.PAUSED

        # There is no plot at the beginning
        self.plot = Plots.NONE

        # There is no GUI loaded at the beginning
        self.is_ctrl_gui_active = False

        plt.ion()

    def init_config(self):
        with self.eth_lock:
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

    def get_gui_lock(self):
        return self.gui_lock

    def get_ffifo_words(self, channels):
        """
        :param channels: 0 or 1, where 0 corresponds to Channels A & B and 1 corresponds to Channels C & D
        :return: the # of words in the fast fifo corresponding to channels
        """
        with self.eth_lock:
            return self.IO.read_ffifo_wd(channels)

    def get_sfifo_words(self):
        with self.eth_lock:
            return self.IO.read_sfifo_wd()

    def get_ffifo_words_cached(self, channels):
        """
        Fulfils the same purpose as get_ffifo_words(), but returns a value that may not accurately reflect the value
        stored in the FPGA at all times. This method serves the purpose of getting the most recently read value without
        needing to send a new command over ethernet.
        :param channels: 0 or 1, where 0 corresponds to Channels A & B and 1 corresponds to Channels C & D
        :return: the # of words in the fast fifo corresponding to channels (cached)
        """

        with self.data_lock:
            if channels == self.ChAB:
                return self.ffifo_ab_words
            elif channels == self.ChCD:
                return self.ffifo_cd_words

    def get_sfifo_words_cached(self):
        """
        See: get_ffifo_words_cached()
        """
        with self.data_lock:
            return self.sfifo_words

    def get_evt_num_cached(self):
        """
        See: get_ffifo_words_cached()
        """
        with self.data_lock:
            return self.evt_num

    def get_mode(self):
        with self.eth_lock:
            return self.IO.read_reg('CR?')

    def set_mode(self, mode):
        """
        :param mode: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('CR', mode) is False: sys.exit()
        time.sleep(0.1)

    def get_afe_gain(self):
        with self.eth_lock:
            return self.IO.read_reg('AFE:CTRL?')

    def set_afe_gain(self, gain):
        """
        :param gain: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('AFE:CTRL', gain) is False: sys.exit()
        time.sleep(0.1)

    def get_bl_len(self):
        with self.eth_lock:
            return self.IO.read_reg('BL:LEN?')

    def set_bl_len(self, bl_len):
        """
        :param bl_len: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('BL:LEN', bl_len) is False: sys.exit()
        time.sleep(0.1)

    def get_evt_len(self):
        with self.eth_lock:
            return self.IO.read_reg('EVT:LEN?')

    def set_evt_len(self, evt_len):
        """
        :param evt_len: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('EVT:LEN', evt_len) is False: sys.exit()
        time.sleep(0.1)

    def get_evt_tail(self):
        with self.eth_lock:
            return self.IO.read_reg('EVT:TAIL?')

    def set_evt_tail(self, evt_tail):
        """
        :param evt_tail: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('EVT:TAIL', evt_tail) is False: sys.exit()
        time.sleep(0.1)

    def get_trig_th(self):
        with self.eth_lock:
            return self.IO.read_reg('TRIG:TH?')

    def set_trig_th(self, trig_th):
        """
        :param trig_th: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('TRIG:TH', trig_th) is False: sys.exit()
        time.sleep(0.1)

    def get_trig_dt(self):
        with self.eth_lock:
            return self.IO.read_reg('TRIG:DT?')

    def set_trig_dt(self, trig_dt):
        """
        :param trig_dt: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('TRIG:DT', trig_dt) is False: sys.exit()
        time.sleep(0.1)

    def get_trig_dl(self):
        with self.eth_lock:
            return self.IO.read_reg('TRIG:DL?')

    def set_trig_dl(self, trig_dl):
        """
        :param trig_dl: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('TRIG:DL', trig_dl) is False: sys.exit()
        time.sleep(0.1)

    def get_bpm_dia(self):
        with self.eth_lock:
            return self.IO.read_reg('BPM:DIA?')

    def set_bpm_dia(self, bpm_dia):
        """
        :param bpm_dia: non-negative integer
        """
        with self.eth_lock:
            if self.IO.write_reg('BPM:DIA', bpm_dia) is False: sys.exit()
        time.sleep(0.1)

    def get_cal_gain(self, channel):
        """
        :param channel: uppercase character corresponding to the appropriate channel, e.g. 'A'
        :return: the cal gain value for channel in IEEE 754 SP floating format
        """
        with self.eth_lock:
            return self.IO.read_reg('CAL:GAIN:' + channel + '?')

    def set_cal_gain(self, channel, cal_gain):
        """
        :param channel: uppercase character corresponding to the appropriate channel, e.g. 'A'
        :param cal_gain: the cal gain value for channel in IEEE 754 SP floating format
        """
        with self.eth_lock:
            if self.IO.write_reg('CAL:GAIN:' + channel, cal_gain) is False: sys.exit()
        time.sleep(0.1)

    def get_ch_gain(self, channel):
        """
        :param channel: uppercase character corresponding to the appropriate channel, e.g. 'A'
        :return: the ch gain value for channel in IEEE 754 SP floating format
        """
        with self.eth_lock:
            return self.IO.read_reg('CH:GAIN:' + channel + '?')

    def set_ch_gain(self, channel, ch_gain):
        """
        :param channel: uppercase character corresponding to the appropriate channel, e.g. 'A'
        :param ch_gain: the ch gain value for channel in IEEE 754 SP floating format
        :return:
        """
        with self.eth_lock:
            if self.IO.write_reg('CH:GAIN:' + channel, ch_gain) is False: sys.exit()
        time.sleep(0.1)

    def rd_flash(self):
        """
        Copies data currently in the flash memory to the flash buffer as well as the FPGA
        """
        with self.eth_lock:
            # First, read from the flash memory, which transfers data from the flash into the flash buffer.
            # Then, transfer the data from the flash buffer to the FPGA. (There is currently no command to directly
            # send data from flash memory to the FPGA)
            if self.IO.write_reg('FLASH:READ', 0) is False: sys.exit()  # the 0 is arbitrary
            time.sleep(0.1)
            if self.IO.write_reg('FLASHBUF:TO:FPGA', 0) is False: sys.exit()  # the 0 is arbitrary
        time.sleep(0.1)

    def wr_flash(self):
        """
        Copies data currently in the FPGA registers to the flash buffer as well as the flash memory
        """
        with self.eth_lock:
            # First, copy data currently in the FPGA to the MicroBlaze flash buffer.
            # Then, copy the data from the flash buffer to the flash memory.
            if self.IO.write_reg('FPGA:TO:FLASHBUF', 0) is False: sys.exit()  # the 0 is arbitrary
            time.sleep(0.1)
            if self.IO.write_reg('FLASH:WRIT', 0) is False: sys.exit()  # the 0 is arbitrary
        time.sleep(0.1)

    def get_mac_address(self, index):
        """
        Get the integer value at index of the MAC address stored in the MicroBlaze flash buffer (see set_mac_address)
        :param index: which portion of the MAC address to read from
        :return: the integer value of that portion [0-255]
        """
        with self.eth_lock:
            return self.IO.read_reg('FL:BUF:MAC:' + str(index) + '?')

    def set_mac_address(self, index, value):
        """
        Writes a new value for the MAC address at position index to the MicroBlaze flash buffer, where index is an
        integer in the range [0, 5] that corresponds to one of the 6 portions of an IP address.
        E.g. for the MAC address 00.01.02.03.04.05, 00 corresponds to index 0, 01 corresponds to index 1, etc.
        Value is an integer in the range [0, 255]

        :param index: which portion of the MAC address to write to
        :param value: the integer value to write
        """
        with self.eth_lock:
            if self.IO.write_reg('FL:BUF:MAC:' + str(index), value) is False: sys.exit()
        time.sleep(0.1)

    def get_ip_address(self, index):
        """
        Get the integer value at index of the IP address stored in the MicroBlaze flash buffer (see set_ip_address)
        :param index: which portion of the IP address to read from
        :return: the integer value of that portion [0-255]
        """
        with self.eth_lock:
            return self.IO.read_reg('FL:BUF:IP:' + str(index) + '?')

    def set_ip_address(self, index, value):
        """
        Writes a new value for the IP address at position index to the MicroBlaze flash buffer, where index is an
        integer in the range [0, 3] that corresponds to one of the 6 portions of an IP address.
        E.g. for the IP address 192.168.13.10, 192 corresponds to index 0, 168 corresponds to index 1, etc.
        Value is an integer in the range [0, 255]

        :param index: which portion of the IP address to write to
        :param value: the integer value to write
        """
        with self.eth_lock:
            if self.IO.write_reg('FL:BUF:IP:' + str(index), value) is False: sys.exit()
        time.sleep(0.1)

    def get_status(self):
        """
        :return: the value of the status register in the FPGA
        """
        with self.eth_lock:
            return self.IO.read_reg('STS?')

    def float_to_int(self, f):
        """
        Returns the integer representation of the IEEE 754 format of the given python
        floating point value.
        For example, 1.0 returns 1065353216
        :param f: Python float
        :return: IEEE 754 formatted integer
        """
        import struct
        return struct.unpack('<i', struct.pack('<f', f))[0]

    def int_to_float(self, i):
        """
        Returns the python floating point representation of the IEEE 754 format integer
        :param i: IEEE 754 formatted integer
        :return: Python float
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
        """
        Sets the current operation mode, which represents whether data is being collected or not
        :param op_mode: The new operation mode (PAUSED or RUNNING)
        """
        self.op_mode = op_mode

    def get_op_mode(self):
        """
        :return: The current operation mode (PAUSED or RUNNING)
        """
        return self.op_mode

    def set_plot(self, plot):
        """
        :param plot: The new active plot.
        """
        self.plot = plot

    def get_plot(self):
        """
        :return: The current active plot.
        """
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
                with self.data_lock:
                    ax.plot(self.time_data, self.s_data)
            else:
                ax1 = fig.add_subplot(211)
                ax2 = fig.add_subplot(212)
                y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
                ax1.yaxis.set_major_formatter(y_formatter)
                ax2.yaxis.set_major_formatter(y_formatter)

                # Disable scientific notation (set to True if need enabled)
                ax1.get_yaxis().get_major_formatter().set_scientific(False)
                ax2.get_yaxis().get_major_formatter().set_scientific(False)
                with self.data_lock:
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
                        ax1.set_ylabel('X/Y position (um)', labelpad=10)
                        ax2.set_ylabel('X/Y res. rms (um)', labelpad=10)
                        ax1.plot(self.time_data, self.x_pos_data, 'b-', label='X pos')
                        ax1.plot(self.time_data, self.y_pos_data, 'r-', label='Y pos')
                        ax2.plot(self.time_data, self.x_rms_data, 'b-', label='X rms')
                        ax2.plot(self.time_data, self.y_rms_data, 'r-', label='Y rms')

                        # Display running average

                        # Label
                        ax1.text(1.02, 0.2, 'X Avg:', transform=ax1.transAxes, fontsize=8)
                        # We need to save this as an attribute so it can be referenced in update_calculations()
                        self.x_pos_avg = ax1.text(1.1, 0.2, str(self.get_average(self.x_pos_data)),
                                                  transform=ax1.transAxes, fontsize=8)

                        ax1.text(1.02, 0.1, 'Y Avg:', transform=ax1.transAxes, fontsize=8)
                        self.y_pos_avg = ax1.text(1.1, 0.1, str(self.get_average(self.y_pos_data)),
                                                  transform=ax1.transAxes, fontsize=8)
                    elif plot == Plots.POWER:
                        ax1.set_title('Power')
                        ax1.set_ylabel('Power AB', labelpad=10)
                        ax2.set_ylabel('Power CD', labelpad=10)
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

                box1 = ax1.get_position()
                box2 = ax2.get_position()
                # Shrink current axis's width by 10% on the right so we can fit a legend there
                ax1.set_position([box1.x0, box1.y0, box1.width * 0.9, box1.height])
                ax2.set_position([box2.x0, box2.y0, box2.width * 0.9, box2.height])
                ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

                # Both axes share the same x label, so we only need one
                ax2.set_xlabel('Time(s)')

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

    def update_calculations(self):
        """
        Updates the active plot by adjusting the x/y axis based on the data collected so far.
        Assumes the plot is one of: Position, Intensity, or Power
        """
        # Only take action if there's an active plot
        if self.get_plot() != Plots.NONE:
            if self.get_plot() == Plots.INTENSITY:
                ax1, = plt.gcf().get_axes()
                with self.data_lock:
                    ax1.get_lines()[0].set_data(self.time_data, self.s_data)
            else:
                ax1, ax2 = plt.gcf().get_axes()
                with self.data_lock:
                    if self.get_plot() == Plots.POSITION:
                        # Update x/y data
                        ax1.get_lines()[0].set_data(self.time_data, self.x_pos_data)
                        ax1.get_lines()[1].set_data(self.time_data, self.y_pos_data)
                        ax2.get_lines()[0].set_data(self.time_data, self.x_rms_data)
                        ax2.get_lines()[1].set_data(self.time_data, self.y_rms_data)
                        # Update averages
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
        """
        Assuming the active plot is the waveform plot, this updates the plot in the same manner as update_calculations().
        Note that this functionality is separated from update_calculations() since the calculations are not necessarily
        updated at the same time as the waveform.
        """
        if self.get_plot() == Plots.WAVEFORM:
            ax1, ax2 = plt.gcf().get_axes()
            with self.data_lock:
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
        self.samples_to_read = 16 * ((self.get_evt_len() - self.get_bl_len() - 4) // 16)
        with self.data_lock:
            self.ffifo_ab_words = self.get_ffifo_words(self.ChAB)
            self.ffifo_cd_words = self.get_ffifo_words(self.ChCD)
            # just like in LabVIEW, waveform data is ready based on occupancy of FFIFO AB
            return self.ffifo_ab_words > self.samples_to_read

    def is_new_data_rdy(self):
        """
        Determines if a a new packet of data is ready to be read from the slow fifo in the FPGA
        :return: True | False
        """
        with self.data_lock:
            self.sfifo_words = self.get_sfifo_words()
            return self.sfifo_words > 16

    def read_data(self):
        """
        Read a packet of data from the slow fifo in the FPGA and update the appropriate data buffers (x, y, etc.)
        """
        with self.eth_lock:
            packet = self.IO.read_buffer('SFIFO:DATA?')  # read one packet from FPGA buffer
        if packet[0] != self.PACKET_ID:
            raise TypeError('Packet ID error!')

        with self.data_lock:
            self.evt_num = packet[1] & 0xFFFF
            # time increments with each data packet
            self.current_time += 1
            # extract new data from packet
            x = TCP.s16(packet[2] >> 16)
            y = TCP.s16(packet[2] & 0xFFFF)
            s = TCP.s16(packet[3] >> 16)
            PA = self.int_to_float(packet[4])
            PB = self.int_to_float(packet[5])
            PC = self.int_to_float(packet[6])
            PD = self.int_to_float(packet[7])

            # add new data to old data
            self.time_data.append(self.current_time)
            self.x_pos_data.append(x)
            self.y_pos_data.append(y)
            self.s_data.append(s)
            self.power_a_data.append(PA)
            self.power_b_data.append(PB)
            self.power_c_data.append(PC)
            self.power_d_data.append(PD)

            x_rms = TCP.rms(self.x_pos_data)
            y_rms = TCP.rms(self.y_pos_data)
            self.x_rms_data.append(x_rms)
            self.y_rms_data.append(y_rms)

    def read_waveform(self):
        """
        Read the fast fifos in the FPGA for waveform data
        """
        with self.eth_lock:
            waveform_AB = self.IO.read_waveform(self.ChAB, self.samples_to_read)
            waveform_CD = self.IO.read_waveform(self.ChCD, self.samples_to_read)
        # False if waveform not successfully read
        with self.data_lock:
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
        with self.data_lock:
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

    def close_plot(self):
        """
        Closes the plot window
        """
        self.set_plot(Plots.NONE)
        plt.close('all')

    def get_ctrl_gui_state(self):
        return self.is_ctrl_gui_active

    def set_ctrl_gui_state(self, state):
        """
        :param state: True | False
        """
        self.is_ctrl_gui_active = state

    def close_windows(self):
        """
        Closes control window and any active plots
        """
        self.close_plot()
        with self.get_gui_lock():
            self.set_ctrl_gui_state(False)

    def shutdown(self):
        self.close_windows()
        self.clear_data()
        with self.eth_lock:
            self.IO.destroy()
        plt.ioff()
