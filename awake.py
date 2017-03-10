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
import logging

# import csv

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

stop_flag = 0
x_pos_data = []


def await_stop():
    while True:
        stop_comm = raw_input('Enter "stop" to stop measuring data: ')
        if stop_comm == 'stop':
            # data_lock.acquire()
            global stop_flag
            stop_flag = 1
            # data_lock.release()
            break
        else:
            print 'The command entered is invalid'


# Updates the graph
def update(axes, data):
    x_pos_data.append(data)
    axes.clear()
    axes.plot(x_pos_data)


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
        #         x = s16(packet[3] >> 16)
        #         y = s16(packet[3] & 0xFFFF)
        #         s = s16(packet[4] >> 16)
        #         PA = packet[5]
        #         PB = packet[6]
        #         PC = packet[7]
        #         PD = packet[8]

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
        user_input_thread = threading.Thread(target=await_stop)
        user_input_thread.start()

        plt.ion()
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)

        while not stop_flag:
            samples_in_sfifo = IO.read_sfifo_wd()
            if samples_in_sfifo > 16:
                packet = IO.read_buffer('SFIFO:DATA?')  # read one packet from FPGA buffer
                if packet[0] != PACKET_ID:
                    print "Packet ID error !"
                x = s16(packet[3] >> 16)
                logging.debug(x)
                update(ax1, x)
                plt.pause(0.05)

        plt.close()
        stop_flag = 0

    else:
        print "Not a valid input!"

# -- end of while loop------------------------------------

IO.destroy()

# ---- end of main --------------------------------------------------
