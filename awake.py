#!/usr/bin/python 
# This is a standalone DAQ/control program for AWAKE BPM SPU box, 
# So far tested with Python 2.7.12 under Windows8/64 bit.
# Oct.27,2016: text mode implemented. 
# Version: 
# awake.py  :  text mode, stable 
# awake1.py: add a seperate thread to detect key press, works, but not great. Nov.23,2016
# awake2.py: text + chart plot mode, not stable

import time
import multiprocessing
import Queue
import logging
import DataProcessor
import Commands

# These are only used to suppress a warning
import warnings
import matplotlib.cbook

# suppress an irrelevant warning that gets printed to the console
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

# configure logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# def get_user_input(command_queue):
#     while True:
#         print """
#         Enter any of the following commands on the left
#         to do the corresponding command on the right:
#         stop        |   to stop measuring data
#         close       |   to close any open plots (but continue measuring data)
#         position    |   to view X/Y data
#         intensity   |   to view S (intensity) data
#         power       |   to view Power AB/CD data
#         rms         |   to view X/Y rms data
#         """
#         command = raw_input('Your command: ')
#
#         command_queue.put(command)
#
#         if command == 'stop':
#             break


def process_data(host, port, command_queue):

    DEFAULT_MODE = 'close'
    POSITION_MODE = 'position'
    INTENSITY_MODE = 'intensity'
    POWER_MODE = 'power'
    RMS_MODE = 'rms'
    STOP_MODE = 'stop'

    data_processor = DataProcessor.DataProcessor(host, port)

    data_processor.init_config()


    while True:
        command = command_queue.get()

        if command == '1':
            data_processor.view_parameters()

        elif command == '2':
            data_processor.view_fifo_occupancy()

        elif command == '3':  # Print&Save ADC waveforms for all four channels
            data_processor.view_waveform()

        # Change this!
        elif (command == '10'):  # Print/Save Packet in consecutive command number

            # time counter
            current_time = 0
            while True:
                try:
                    command = command_queue.get(block=False)
                    data_processor.set_mode(command)
                except Queue.Empty:
                    pass

                if data_processor.read_data(current_time):
                    current_time += 1
                    current_mode = data_processor.get_mode()
                    if current_mode == DEFAULT_MODE:
                        data_processor.close_windows()
                    elif (current_mode == POSITION_MODE or
                                  current_mode == INTENSITY_MODE or
                                  current_mode == POWER_MODE or
                                  current_mode == RMS_MODE):
                        # check if either no window was open previously or the previous mode was different
                        if data_processor.new_plot_needed():
                            # logging.info('Creating new plot...')
                            data_processor.setup_plot()
                        else:  # update
                            # logging.info('Updating current plot...')
                            data_processor.update_plot()

                    else:  # STOP_MODE
                        break

            data_processor.close_windows()
            data_processor.clear_data()

            # Set mode to default before finishing
            data_processor.set_mode(DataProcessor.DataProcessor.DEFAULT_MODE)

        elif command == 'finish':
            data_processor.shutdown()
            break

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
        print("Not a valid input!")

    host += str(IP)
    print "The DSP IP address is: ", host

    command_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=process_data, args=(host, port, command_queue))
    p.start()

    # Give time for other process to do its initial config
    time.sleep(1)

    while True:
        try:
            print """
            Enter the number next to your desired command:
            (1) Start Measuring Data
            (2) Pause Measuring Data
            (3) Clear Data
            (4) Edit Settings
            (5) View Waveform Data
            (6) View Position Data
            (7) View Intensity Data
            (8) View Power Data
            (9) Close Windows
            (10) Exit
            """
            command = int(raw_input('Your command: '))

        except ValueError:
            print("Not a valid command!")
            continue

        if command < 1 or command > 10:
            print 'Not a valid command!'
        else:
            command_queue.put(command)

        if command == 10:
            break


        # elif command == '4':  # change AFE gain setting
        #     pass
            # try:
            #     Gain = int(raw_input('Enter AFE gain: 1 ~ 31 dB Attenuation:\n'))
            # except ValueError:
            #     print("not a valid input!")
            # if (Gain > 0) and (Gain < 32):
            #     # if IO.write_reg('AFE:CTRL', Gain) is False: exit()
            #     # command_queue.put()
            #     print "The new AFE gain is (dB): ", -1 * Gain
            # else:
            #     print "gain value not valid!"
            #

        # elif command == '5':  # Trigger mode
        #     try:
        #         Trig_mode = int(raw_input('Enter trigger mode: 0=external, 1=internal, 2=self, 3=Cal:\n'))
        #     except ValueError:
        #         print("not a valid input!")
        #         Trig_mode = 10  # fake,make it invalid
        #
        #     command_queue.put()
            # if (Trig_mode == 0):
            #     print "The new trigger mode is: External"
            #     if IO.write_reg('CR', MODE_EXT_TRIG) is False: exit()
            # elif (Trig_mode == 1):
            #     print "The new trigger mode is: Internal"
            #     if IO.write_reg('CR', MODE_INT_TRIG) is False: exit()
            # elif (Trig_mode == 2):
            #     print "The new trigger mode is: Self"
            #     if IO.write_reg('CR', MODE_SEL_TRIG) is False: exit()
            # elif (Trig_mode == 3):
            #     print "The new trigger mode is: Cal+Internal"
            #     if IO.write_reg('CR', MODE_CAL) is False: exit()
            # else:
            #     print "Input value not valid!"


        # elif command == '6':  # change trigger delay in unit of 10 ns
        #
        #     try:
        #         TRIG_DL = int(raw_input('Enter trigger delay 0~ 64000 :\n'))
        #     except ValueError:
        #         print("not a valid input!")
        #     if (TRIG_DL > 0) and (TRIG_DL < 64000):
        #         if IO.write_reg('TRIG:DL', TRIG_DL) is False: exit()
        #         print "The new trigger delay is (ns): ", TRIG_DL * 10
        #     else:
        #         print "gain value not valid!"



    # -- end of while loop------------------------------------
    # tell process to finish
    # command_queue.put('finish')
    p.join()
# ---- end of main --------------------------------------------------
