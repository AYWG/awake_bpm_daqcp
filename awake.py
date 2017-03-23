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
import Modes
import Plots

# These are only used to suppress a warning
import warnings
import matplotlib.cbook

# suppress an irrelevant warning that gets printed to the console
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

# configure logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def process_data(host, port, command_queue):

    data_processor = DataProcessor.DataProcessor(host, port)
    data_processor.init_config()

    while True:
        command = command_queue.get()

        if command == Commands.START_MEASURING_DATA:
            data_processor.set_op_mode(Modes.RUNNING)

        elif command == Commands.PAUSE_MEASURING_DATA:
            data_processor.set_op_mode(Modes.PAUSED)

        elif command == Commands.CLEAR_DATA:
            data_processor.clear_data()

        elif command == Commands.EDIT_SETTINGS:
            # implement this later
            pass

        elif command == Commands.VIEW_WAVEFORM_DATA:
            data_processor.setup_plot(Plots.WAVEFORM)

        elif command == Commands.VIEW_POSITION_DATA:
            data_processor.setup_plot(Plots.POSITION)

        elif command == Commands.VIEW_INTENSITY_DATA:
            data_processor.setup_plot(Plots.INTENSITY)

        elif command == Commands.VIEW_POWER_DATA:
            data_processor.setup_plot(Plots.POWER)

        elif command == Commands.CLOSE_WINDOWS:


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

    # -- end of while loop------------------------------------
    # tell process to finish
    # command_queue.put('finish')
    p.join()
# ---- end of main --------------------------------------------------
