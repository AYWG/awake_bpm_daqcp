import wx
import threading
import time
import CtrlWindow


class CtrlFrame(wx.Frame):
    """
    Top level frame for the GUI. Has one child window (CtrlWindow) that houses all of the different panels.
    """

    def __init__(self, parent, title, data_processor):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title=title)
        self.data_processor = data_processor

        self.ctrl_window = CtrlWindow.CtrlWindow(parent=self, data_processor=data_processor)
        self.__set_properties()
        self.__do_layout()

        self.__attach_events()
        self.t = threading.Thread(target=self._check_for_close_signal)
        self.t.start()

    def __set_properties(self):
        # Light-grey
        # self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))

    def __do_layout(self):
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(self.ctrl_window, 1, wx.EXPAND)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

        # Set the minimum size of the window once all of the sizers have been set up.
        display_size = wx.DisplaySize()
        self.SetMinSize((display_size[0]/2, display_size[1]/2))

    def __attach_events(self):
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def get_thread(self):
        return self.t

    def _check_for_close_signal(self):
        """
        Worker thread that checks if the GUI should still be open
        """
        while True:
            if self:
                if not self.data_processor.get_ctrl_gui_state():
                    wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_CLOSE.typeId, self.GetId()))
                    break
                time.sleep(0.5)
            else:
                break

    def OnClose(self, event):
        with self.data_processor.get_gui_lock():
            self.data_processor.set_ctrl_gui_state(False)
            self.ctrl_window.fifo_occupancy_panel.set_stop_flag(True)
            self.ctrl_window.event_num_panel.set_stop_flag(True)

        # Need to wait until all child threads terminate before destroying the GUI
        self.ctrl_window.fifo_occupancy_panel.get_thread().join()
        self.ctrl_window.event_num_panel.get_thread().join()
        self.get_thread().join()
        self.Destroy()