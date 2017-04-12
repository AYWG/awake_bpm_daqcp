#!/usr/bin/python 
# This is a standalone DAQ/control program for AWAKE BPM SPU box, 
# So far tested with Python 2.7.12 under Windows8/64 bit.
# Oct.27,2016: text mode implemented. 
# Version: 
# awake.py  :  text mode, stable 
# awake1.py: add a seperate thread to detect key press, works, but not great. Nov.23,2016
# awake2.py: text + chart plot mode, not stable

import time
import threading
import multiprocessing
import logging
import DataProcessor
import Commands
import Modes
import Plots
import CtrlGUI

# configure logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def data_collector(data_processor, command_queue, lock):
    """
    thread that reads from the FPGA and updates the plots
    :param data_processor:
    :param command_queue:
    :param lock:
    :return:
    """
    while True:
        # Roughly the same logic as in LabVIEW
        if data_processor.is_waveform_rdy():
            with lock:
                if data_processor.get_op_mode() == Modes.RUNNING:
                    data_processor.read_waveform()
                    command_queue.put(Commands.UPDATE_WAVEFORM)
                    if data_processor.is_new_data_rdy():
                        data_processor.read_data()
                        command_queue.put(Commands.UPDATE_CALCULATIONS)
                else:
                    break
        else:
            command_queue.put(Commands.REFRESH_PLOT)
            time.sleep(0.5)


def is_thread_active(name):
    """
    Checks if there's a thread that's alive and has the given name
    :param name: name of thread to search for
    :return: True | False
    """
    for t in threading.enumerate():
        if t.name == name:
            return True
    return False


def ctrl_gui_handler(data_processor):
    """
    Creates the control GUI and keeps it running until the user closes it
    :param data_processor:
    :return:
    """
    data_processor.set_ctrl_gui_state(True)
    gui = CtrlGUI.CtrlGUI(data_processor)
    gui.MainLoop()


def plot_refresher(data_processor, command_queue, lock):
    """
    For refreshing the plot while data is not being collected
    :param data_processor:
    :param command_queue:
    :return:
    """
    while True:
        with lock:
            if data_processor.get_op_mode() == Modes.PAUSED:
                command_queue.put(Commands.REFRESH_PLOT)
            else:
                break
        time.sleep(0.5)


def process_data(host, port, command_queue):
    data_processor = DataProcessor.DataProcessor(host, port)
    data_processor.init_config()

    op_mode_lock = threading.Lock()

    import Tkinter as tk # for the exception

    while True:
        try:
            command = command_queue.get()

            if command == Commands.START_MEASURING_DATA:
                # only take action if currently paused
                if data_processor.get_op_mode() == Modes.PAUSED:
                    op_mode_lock.acquire()
                    data_processor.set_op_mode(Modes.RUNNING)
                    op_mode_lock.release()
                    t_data_collector = threading.Thread(target=data_collector,
                                                        args=(data_processor, command_queue, op_mode_lock),
                                                        name='data_collector')
                    t_data_collector.start()

            elif command == Commands.PAUSE_MEASURING_DATA:
                # only take action if currently running
                if data_processor.get_op_mode() == Modes.RUNNING:
                    op_mode_lock.acquire()
                    data_processor.set_op_mode(Modes.PAUSED)
                    op_mode_lock.release()

            elif command == Commands.CLEAR_DATA:
                data_processor.clear_data()

            elif command == Commands.EDIT_SETTINGS:
                # Only one settings window active
                if not is_thread_active('ctrl_gui_handler'):
                    t_ctrl_gui_handler = threading.Thread(target=ctrl_gui_handler, args=(data_processor,),
                                                          name='ctrl_gui_handler')
                    t_ctrl_gui_handler.start()

            elif command == Commands.VIEW_WAVEFORM_DATA:
                data_processor.setup_plot(Plots.WAVEFORM)

            elif command == Commands.VIEW_POSITION_DATA:
                data_processor.setup_plot(Plots.POSITION)

            elif command == Commands.VIEW_INTENSITY_DATA:
                data_processor.setup_plot(Plots.INTENSITY)

            elif command == Commands.VIEW_POWER_DATA:
                data_processor.setup_plot(Plots.POWER)

            elif command == Commands.CLOSE_WINDOWS:
                data_processor.close_windows()

            elif command == Commands.UPDATE_CALCULATIONS:
                data_processor.update_calculations()

            elif command == Commands.UPDATE_WAVEFORM:
                data_processor.update_waveform()

            elif command == Commands.REFRESH_PLOT:
                data_processor.enable_plot_interaction()

            elif command == Commands.EXIT:
                data_processor.shutdown()
                break

            if (data_processor.get_plot() != Plots.NONE and
                data_processor.get_op_mode() == Modes.PAUSED and not
                is_thread_active('plot_refresher')):

                t_plot_refresher = threading.Thread(target=plot_refresher,
                                                    args=(data_processor, command_queue, op_mode_lock),
                                                    name='plot_refresher')
                t_plot_refresher.start()

        except tk.TclError:
            # Will get this error if trying to close the plot window via the 'X' button
            # Thus, we catch it and do what is intended by the user
            data_processor.close_plot()


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

    # Get the IP address of the connected BPM
    try:
        IP = int(raw_input('Enter DSP IP address (last number 2 ~ 254):'))
        if (IP > 255) or (IP < 2) is True:
            print "IP address out of range!"
            exit()
    except ValueError:
        print("Not a valid input!")

    host += str(IP)
    print "The DSP IP address is: ", host

    # Need a synchronized queue to process commands from the user (as well as some internal commands)
    command_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=process_data, args=(host, port, command_queue))
    p.start()

    # Give time for other process to do its initial config
    time.sleep(1)

    # Continuously ask for user input until termination
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

        if command == Commands.EXIT:
            break

    # -- end of while loop------------------------------------
    # Wait until other process finishes
    p.join()
# ---- end of main --------------------------------------------------
