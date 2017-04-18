import wx
import threading
import time


class EventNumPanel(wx.Panel):
    """
    Panel that displays the current event number
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor

        self.lbl_event_num = wx.StaticText(self, wx.ID_ANY, 'Event #')
        self.txt_event_num = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_READONLY)
        self.event_num_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()
        # self.t = threading.Thread(target=self._update_event_num)
        # self.t.start()

    def __set_properties(self):
        # no special properties
        pass

    def __do_layout(self):
        sizer_event_num_box = wx.StaticBoxSizer(self.event_num_box, wx.VERTICAL)

        sizer_event_num = wx.BoxSizer(wx.HORIZONTAL)
        sizer_event_num.Add(self.lbl_event_num, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_event_num.Add(self.txt_event_num, 2, wx.EXPAND, 0)

        sizer_event_num_box.Add(sizer_event_num, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_event_num_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        pass

    def initialize_controls(self):
        self.txt_event_num.SetValue(str(self.data_processor.get_evt_num_cached()))

    def _update_event_num(self):
        """
        Worker thread that checks the current event # and updates the value displayed in the GUI
        """
        while True:
            if self:
                self.txt_event_num.SetValue(str(self.data_processor.get_evt_num_cached()))
                time.sleep(0.5)
            else:
                break

    def update_event_num(self):
        self.txt_event_num.SetValue(str(self.data_processor.get_evt_num_cached()))
