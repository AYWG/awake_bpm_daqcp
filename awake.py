#!/usr/bin/python 
# This is a standalone DAQ/control program for AWAKE BPM SPU box, 
# So far tested with Python 2.7.12 under Windows8/64 bit.
# Oct.27,2016: text mode implemented. 
# Version: 
# awake.py  :  text mode, stable 
# awake1.py: add a seperate thread to detect key press, works, but not great. Nov.23,2016
# awake2.py: text + chart plot mode, not stable

from TCP import *
import matplotlib.pyplot as plt
import numpy as np
import time
import threading

# import csv

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# These are only used to suppress a warning
import warnings
import matplotlib.cbook

# suppress an irrelevant warning that gets printed to the console
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)


# DEBUG = False
DEBUG = True

host = "192.168.13."
port = 23

try:
    IP = int(raw_input('Enter DSP IP address (last number 2 ~ 254):'))
    if (IP > 255) or (IP < 2) is True:
        print "IP address out of range!"
        exit()
except ValueError:
    print("not a valid input!")
host = host + str(IP)
print "the DSP IP addr is:", host

# -------------------------------------------------------------------------------
BPM_DIA = 40

TRIG_TH = 200  # only used for self trigger mode
TRIG_DT = 0
TRIG_DL = 0
EVT_LEN = 1024
EVT_TAIL = 300
BL_LEN = 40

MODE_INT_TRIG = 0x105  # mode reg bit = RUN + Internal trigger + BLR readout
MODE_EXT_TRIG = 0x101  # mode reg bit = RUN + External trigger + BLR readout  
MODE_SEL_TRIG = 0x103  # mode reg bit = RUN + Self trigger + BLR readout
MODE_CAL = 0x2105  # mode reg bit = RUN + Self trigger + BLR readout + AFE Cal.

MODE_TEMP = 0x0020  # mode reg bit = Ena temperature reading

A1dB = 0x01  # Analog Front-end board gain setting : 1 dB attenuation
A2dB = 0x02  # Analog Front-end board gain setting : 2 dB attenuation
A4dB = 0x04  # Analog Front-end board gain setting : 4 dB attenuation
A8dB = 0x08  # Analog Front-end board gain setting : 8 dB attenuation
A16dB = 0x10  # Analog Front-end board gain setting : 16 dB attenuation

Gain = A1dB + A2dB + A4dB + A8dB + A16dB
# --------------------------------------------------------------------------------

ChAB = 0
ChCD = 1
PACKET_ID = 0x4142504D
IO = TCP(host, port)
print IO.read_MBver()

# -----------------------------------------------------------------------
# Configure parameters
if IO.write_reg('BPM:DIA', BPM_DIA) is False: exit()
time.sleep(0.1)
if IO.write_reg('TRIG:TH', TRIG_TH) is False: exit()
time.sleep(0.1)
if IO.write_reg('TRIG:DT', TRIG_DT) is False: exit()
time.sleep(0.1)
if IO.write_reg('TRIG:DL', TRIG_DL) is False: exit()
time.sleep(0.1)
if IO.write_reg('EVT:LEN', EVT_LEN) is False: exit()
time.sleep(0.1)
if IO.write_reg('EVT:TAIL', EVT_TAIL) is False: exit()
time.sleep(0.1)
if IO.write_reg('BL:LEN', BL_LEN) is False: exit()
time.sleep(0.1)
print 'BPM Diameter (mm) = ', format(IO.read_reg('BPM:DIA?'), 'd')
print 'TRIG:TH =', format(IO.read_reg('TRIG:TH?'), 'd')
print 'TRIG:DT =', format(IO.read_reg('TRIG:DT?'), 'd')
print 'TRIG:DL =', format(IO.read_reg('TRIG:DL?'), 'd')
print 'EVT:LEN =', format(IO.read_reg('EVT:LEN?'), 'd')
print 'EVT:TAIL =', format(IO.read_reg('EVT:TAIL?'), 'd')
print 'BL:LEN =', format(IO.read_reg('BL:LEN?'), 'd')

if IO.write_reg('AFE:CTRL', Gain) is False: exit()
time.sleep(0.1)
if IO.write_reg('CR', MODE_EXT_TRIG) is False: exit()
time.sleep(0.1)
print 'AFE Ctrl Reg = 0x', format(IO.read_reg('AFE:CTRL?'), '02x')
print 'Mode Reg = 0x', format(IO.read_reg('CR?'), '02x')
# -------------------------------------------------------------------------

# ------------------------------------------------------
evt_file = None

DEFAULT_MODE = 'close'
POSITION_MODE = 'position'
INTENSITY_MODE = 'intensity'
POWER_MODE = 'power'
RMS_MODE = 'rms'
STOP_MODE = 'stop'

current_mode = DEFAULT_MODE

time_data = []
x_pos_data = []
y_pos_data = []
s_data = []
power_a_data = []
power_b_data = []
power_c_data = []
power_d_data = []
x_rms_data = []
y_rms_data = []


def get_user_input():
    while True:
        print """
        Enter any of the following commands on the left
        to do the corresponding action on the right:
        stop        |   to stop measuring data
        close       |   to close any open plots (but continue measuring data)
        position    |   to view X/Y data
        intensity   |   to view S (intensity) data
        power       |   to view Power AB/CD data
        rms         |   to view X/Y rms data
        """
        comm = raw_input('Your command: ')
        print 'Your input is: ', comm
        global current_mode

        if comm == 'stop':
            current_mode = STOP_MODE
            break
        elif comm == 'close':
            current_mode = DEFAULT_MODE
        elif comm == 'position':
            current_mode = POSITION_MODE
        elif comm == 'intensity':
            current_mode = INTENSITY_MODE
        elif comm == 'power':
            current_mode = POWER_MODE
        elif comm == 'rms':
            current_mode = RMS_MODE
        else:
            print 'The command entered is invalid'


# Updates the graph
def update(axes, line, data):
    # update the x/y data
    line.set_data(time_data, data)
    # recompute the data limits
    axes.relim()
    # scale the view based on the new data limits
    axes.autoscale_view()


def update_plot():
    if current_mode == INTENSITY_MODE:
        ax1, = plt.gcf().get_axes()
        ax1.get_lines()[0].set_data(time_data, s_data)
    else:
        ax1, ax2 = plt.gcf().get_axes()
        if current_mode == POSITION_MODE:
            ax1.get_lines()[0].set_data(time_data, x_pos_data)
            ax2.get_lines()[0].set_data(time_data, y_pos_data)
        elif current_mode == POWER_MODE:
            ax1.get_lines()[0].set_data(time_data, power_a_data)
            ax1.get_lines()[1].set_data(time_data, power_b_data)
            ax2.get_lines()[0].set_data(time_data, power_c_data)
            ax2.get_lines()[1].set_data(time_data, power_d_data)
        elif current_mode == RMS_MODE:
            ax1.get_lines()[0].set_data(time_data, x_rms_data)
            ax2.get_lines()[0].set_data(time_data, y_rms_data)

    ax1.relim()
    ax1.autoscale_view()

    # if ax2 is defined
    if 'ax2' in locals():
        ax2.relim()
        ax2.autoscale_view()

    plt.pause(0.1)


def setup_plot():
    # clear the figure
    fig = plt.gcf()
    logging.info('figure retrieved')
    plt.clf()
    logging.info('figure cleared')
    if current_mode == INTENSITY_MODE:
        # ax = plt.subplot(111)
        ax = fig.add_subplot(111)
        ax.set_ylabel('S Intensity')
        ax.set_xlabel('Time (s)')
        ax.set_gid(current_mode)
        line_s, = ax.plot(time_data, s_data)
    else:
        # fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        if current_mode == POSITION_MODE:
            ax1.set_ylabel('X position (um)')
            ax2.set_ylabel('Y position (um)')
            line_x_pos, = ax1.plot(time_data, x_pos_data)
            line_y_pos, = ax2.plot(time_data, y_pos_data)
        elif current_mode == POWER_MODE:
            ax1.set_ylabel('Power AB')
            ax2.set_ylabel('Power CD')
            line_power_a, = ax1.plot(time_data, power_a_data, 'b-', label='A')
            line_power_b, = ax1.plot(time_data, power_b_data, 'r-', label='B')
            line_power_c, = ax2.plot(time_data, power_c_data, 'b-', label='C')
            line_power_d, = ax2.plot(time_data, power_d_data, 'r-', label='D')
            ax1.legend()
            ax2.legend()
        elif current_mode == RMS_MODE:
            ax1.set_ylabel('X res. rms (um)')
            ax2.set_ylabel('Y res. rms (um)')
            line_x_rms, = ax1.plot(time_data, x_rms_data)
            line_y_rms, = ax2.plot(time_data, y_rms_data)

        # gid is only set for the first axes (it would be the same for the second)
        ax1.set_gid(current_mode)
        ax2.set_xlabel('Time(s)')


while True:
    try:
        comm = raw_input(
            'Enter action number(1=settings, 2= FIFOs, 3=waveform, 4=AFE gain, 5=Trig mode, 6=Trig Delay, 9=exit, others(>10)=event taking):')
        print "your input is : ", comm
        action = int(comm)
    except ValueError:
        print("not a valid input!")
        action = 10000  # a fake aciton, make it in-valid

    if action == 1:
        print 'BPM Diameter (mm) = ', format(IO.read_reg('BPM:DIA?'), 'd')
        print 'TRIG:TH =', format(IO.read_reg('TRIG:TH?'), 'd')
        print 'TRIG:DT =', format(IO.read_reg('TRIG:DT?'), 'd')
        print 'TRIG:DL =', format(IO.read_reg('TRIG:DL?'), 'd')
        print 'EVT:LEN =', format(IO.read_reg('EVT:LEN?'), 'd')
        print 'EVT:TAIL =', format(IO.read_reg('EVT:TAIL?'), 'd')
        print 'BL:LEN =', format(IO.read_reg('BL:LEN?'), 'd')
        print 'AFE Ctrl Reg = 0x', format(IO.read_reg('AFE:CTRL?'), '02x')
        print 'Mode Reg = 0x', format(IO.read_reg('CR?'), '02x')

    elif action == 2:
        print 'Fast FIFO occupancy = ', IO.read_ffifo_wd(0)
        print 'Packet FFIFO occupancy = ', IO.read_sfifo_wd()

    elif action == 3:  # Print&Save ADC waveforms for all four channels
        samples_to_read = 16 * ((EVT_LEN - BL_LEN - 4) // 16)
        samples_in_buf = IO.read_ffifo_wd(0)
        print "Fast FIFO occupancy: ", samples_in_buf
        if samples_in_buf > samples_to_read:
            waveform = IO.read_waveform(ChAB, samples_to_read)
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
            waveform = IO.read_waveform(ChCD, samples_to_read)
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

    elif action == 4:  # change AFE gain setting
        try:
            Gain = int(raw_input('Enter AFE gain: 1 ~ 31 dB Attenuation:\n'))
        except ValueError:
            print("not a valid input!")
        if (Gain > 0) and (Gain < 32):
            if IO.write_reg('AFE:CTRL', Gain) is False: exit()
            print "The new AFE gain is (dB): ", -1 * Gain
        else:
            print "gain value not valid!"

    elif action == 5:  # Trigger mode
        try:
            Trig_mode = int(raw_input('Enter trigger mode: 0=external, 1=internal, 2=self, 3=Cal:\n'))
        except ValueError:
            print("not a valid input!")
            Trig_mode = 10  # fake,make it invalid
        if (Trig_mode == 0):
            print "The new trigger mode is: External"
            if IO.write_reg('CR', MODE_EXT_TRIG) is False: exit()
        elif (Trig_mode == 1):
            print "The new trigger mode is: Internal"
            if IO.write_reg('CR', MODE_INT_TRIG) is False: exit()
        elif (Trig_mode == 2):
            print "The new trigger mode is: Self"
            if IO.write_reg('CR', MODE_SEL_TRIG) is False: exit()
        elif (Trig_mode == 3):
            print "The new trigger mode is: Cal+Internal"
            if IO.write_reg('CR', MODE_CAL) is False: exit()
        else:
            print "Input value not valid!"

    elif action == 6:  # change trigger delay in unit of 10 ns
        try:
            TRIG_DL = int(raw_input('Enter trigger delay 0~ 64000 :\n'))
        except ValueError:
            print("not a valid input!")
        if (TRIG_DL > 0) and (TRIG_DL < 64000):
            if IO.write_reg('TRIG:DL', TRIG_DL) is False: exit()
            print "The new trigger delay is (ns): ", TRIG_DL * 10
        else:
            print "gain value not valid!"

    elif action == 9:  # exit
        break

    # Change this!
    elif (action > 9) and (action < 5001):  # Print/Save Packet in consecutive action number

        # evt_file = raw_input('Press RETURN or Enter event file name:')
        # print "New event file name is : ", evt_file
        # if evt_file == '':
        #     print "Event data will NOT be saved to file since no file name provided!"
        #     save_data = False
        # else:
        #     f = open(evt_file, "a")
        #     save_data = True

        # i = 0
        # ticks_old = time.time()
        # x_his = []
        # y_his = []


        # while (i < action):
        #     samples_in_sfifo = IO.read_sfifo_wd()
        #     if samples_in_sfifo > 16:
        #         i = i + 1
        #         ticks = time.time()
        #         event_int = int(ticks - ticks_old)
        #         ticks_old = ticks
        #         packet = IO.read_buffer('SFIFO:DATA?')  # read one packet from FPGA buffer
        #
        #         if packet[0] != PACKET_ID:
        #             print "Packet ID error !"
        #         evt_id = packet[0]
        #         evt_no = packet[1] & 0xFFFF
        #         status_reg = packet[2] >> 16

        # x_his.append(x)
        # y_his.append(y)
        # x_rms = int(rms(x_his))
        # y_rms = int(rms(y_his))

        # print "Event#=", evt_no, "Event interval(seconds)=", event_int, "x(um)=", x, "x_rms(um)=", format(x_rms,
        #                                                                                                   'd'), "y(um)=", y, "y_rms(um)=", format(
        #     y_rms, 'd'), "s=", s, "status=", status_reg

        # if save_data:
        #     try:
        #         f.write('%x\t%d\t%d\t%d\t%d\t%d\t%x\t%x\t%x\t%x\t%d\n' % (
        #         evt_id, evt_no, event_int, x, y, s, PA, PB, PC, PD, status_reg))
        #     except TypeError as e:
        #         print "write file error: ", e

        # if save_data:
        #     f.close()
        #     print "Event data saved to file: ", evt_file


        # spawn a thread for checking user input
        user_input_thread = threading.Thread(target=get_user_input)
        user_input_thread.start()

        plt.ion()

        # time counter
        t = 0
        while current_mode != STOP_MODE:
            samples_in_sfifo = IO.read_sfifo_wd()
            if samples_in_sfifo > 16:
                # print current_mode
                t += 1
                packet = IO.read_buffer('SFIFO:DATA?')  # read one packet from FPGA buffer
                if packet[0] != PACKET_ID:
                    print "Packet ID error !"

                # extract new data from packet
                x = s16(packet[3] >> 16)
                y = s16(packet[3] & 0xFFFF)
                s = s16(packet[4] >> 16)
                PA = packet[5]
                PB = packet[6]
                PC = packet[7]
                PD = packet[8]

                # add new data to old data
                time_data.append(t)
                x_pos_data.append(x)
                y_pos_data.append(y)
                s_data.append(s)
                power_a_data.append(PA)
                power_b_data.append(PB)
                power_c_data.append(PC)
                power_d_data.append(PD)

                x_rms = int(rms(x_pos_data))
                y_rms = int(rms(y_pos_data))
                x_rms_data.append(x_rms)
                y_rms_data.append(y_rms)

                # this needs to be modified
                # check here to update the appropriate plots based on the whichever plot the user wants to view
                if current_mode == DEFAULT_MODE:
                    plt.close()
                elif (current_mode == POSITION_MODE or
                              current_mode == INTENSITY_MODE or
                              current_mode == POWER_MODE or
                              current_mode == RMS_MODE):
                    # check if either no window was open previously or the previous mode was different
                    if not plt.get_fignums() or plt.gcf().get_axes()[0].get_gid() != current_mode:
                        logging.info('Creating new plot...')
                        setup_plot()
                    else:  # update
                        logging.info('Updating current plot...')
                        update_plot()

                else:  # STOP_MODE
                    break

        plt.close()

        # clear data
        del time_data[:]
        del x_pos_data[:]
        del y_pos_data[:]
        del s_data[:]
        del power_a_data[:]
        del power_b_data[:]
        del power_c_data[:]
        del power_d_data[:]
        del x_rms_data[:]
        del y_rms_data[:]

        # Set mode to default before finishing
        current_mode = DEFAULT_MODE

    else:
        print "Not a valid input!"

# -- end of while loop------------------------------------

IO.destroy()

# ---- end of main --------------------------------------------------
