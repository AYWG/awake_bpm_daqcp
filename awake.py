#!/usr/bin/python 
# This is a standalone DAQ/control program for AWAKE BPM SPU box, 
# So far tested with Python 2.7.12 under Windows8/64 bit.
# Oct.27,2016: text mode implemented. 
# Version: 
# awake.py  :  text mode, stable 
# awake1.py: add a seperate thread to detect key press, works, but not great. Nov.23,2016
# awake2.py: text + chart plot mode, not stable

import time
from multiprocessing import Process, Queue, Lock

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# These are only used to suppress a warning
import warnings
import matplotlib.cbook

# suppress an irrelevant warning that gets printed to the console
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

from TCP import *
import DataProcessor


def get_user_input(command_queue):
    while True:
        print """
        Enter any of the following commands on the left
        to do the corresponding command on the right:
        stop        |   to stop measuring data
        close       |   to close any open plots (but continue measuring data)
        position    |   to view X/Y data
        intensity   |   to view S (intensity) data
        power       |   to view Power AB/CD data
        rms         |   to view X/Y rms data
        """
        command = raw_input('Your command: ')

        command_queue.put(command)

        if command == 'stop':
            break


def process_data(host, port, command_queue, output_lock):

    data_processor = DataProcessor.DataProcessor(host, port)

    output_lock.acquire()
    data_processor.init_config()
    output_lock.release()

    while True:
        command = command_queue.get()

        if command == '1':
            output_lock.acquire()
            data_processor.view_parameters()
            output_lock.release()

        elif command == '2':
            output_lock.acquire()
            data_processor.view_fifo_occupancy()
            output_lock.release()

        elif command == '3':  # Print&Save ADC waveforms for all four channels
            output_lock.acquire()
            data_processor.view_waveform()
            output_lock.release()

        elif command == '4':  # change AFE gain setting
            pass

        elif command == '5':  # Trigger mode
            pass

        elif command == '6':  # change trigger delay in unit of 10 ns
            pass

        elif command == '9':  # exit
            break

        # Change this!
        elif (command > 9) and (command < 5001):  # Print/Save Packet in consecutive command number

            # time counter
            t = 0
            while True:
                try:
                    command = command_queue.get(block=False)

                    if command == 'close':
                        data_processor.close_windows()
                except Queue.Empty:
                    pass

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

            # Set mode to default before finishing
            data_processor.set_mode(DataProcessor.DataProcessor.DEFAULT_MODE)

        elif command == 'finish':
            data_processor.shutdown()

        else:
            print "Not a valid input!"

# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


if __name__ == '__main__':
    # Constants
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

    # lock for printing to standard output (helps avoid jumbled output messages)
    output_lock = Lock()

    # Start subprocess here
    command_queue = Queue()
    p = Process(target=process_data, args=(host, port, command_queue, output_lock))
    p.start()

    # Check for user input now
    while True:
        try:
            command = raw_input(
                'Enter command number(1=View Parameters, 2= FIFOs, 3=waveform, 4=AFE gain, 5=Trig mode, 6=Trig Delay, 9=exit, others(>10)=event taking):')
            print "your input is : ", command
        except ValueError:
            print("not a valid input!")
            command = 'invalid'  # a fake aciton, make it in-valid

        if command == '1':
            command_queue.put(command)

        elif command == '2':
            command_queue.put(command)

        elif command == '3':  # Print&Save ADC waveforms for all four channels
            command_queue.put(command)
            pass

        elif command == '4':  # change AFE gain setting
            """
            try:
                Gain = int(raw_input('Enter AFE gain: 1 ~ 31 dB Attenuation:\n'))
            except ValueError:
                print("not a valid input!")
            if (Gain > 0) and (Gain < 32):
                # if IO.write_reg('AFE:CTRL', Gain) is False: exit()
                # command_queue.put()
                print "The new AFE gain is (dB): ", -1 * Gain
            else:
                print "gain value not valid!"
            """

        elif command == '5':  # Trigger mode
            """
            try:
                Trig_mode = int(raw_input('Enter trigger mode: 0=external, 1=internal, 2=self, 3=Cal:\n'))
            except ValueError:
                print("not a valid input!")
                Trig_mode = 10  # fake,make it invalid

            # command_queue.put()
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

            """

        elif command == '6':  # change trigger delay in unit of 10 ns
            """
            try:
                TRIG_DL = int(raw_input('Enter trigger delay 0~ 64000 :\n'))
            except ValueError:
                print("not a valid input!")
            if (TRIG_DL > 0) and (TRIG_DL < 64000):
                if IO.write_reg('TRIG:DL', TRIG_DL) is False: exit()
                print "The new trigger delay is (ns): ", TRIG_DL * 10
            else:
                print "gain value not valid!"
            """

        elif command == '9':  # exit
            break

        # Change this!
        elif command == '10':  # Print/Save Packet in consecutive command number

            get_user_input()
            command_queue.put(command)

            """
            plt.ion()
            # time counter
            t = 0
            while current_mode != STOP_MODE:


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

            # Set mode to default before finishing
            current_mode = DEFAULT_MODE
            """
        else:
            print "Not a valid input!"

    # -- end of while loop------------------------------------
    # tell process to finish
    command_queue.put('finish')
    p.join()

# ---- end of main --------------------------------------------------
