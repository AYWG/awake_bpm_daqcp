import wx
import threading
import time


class FIFOOccupancyPanel(wx.Panel):
    """
    Panel that displays the current occupancy (ie. the number of words) of the fast and slow FIFOs
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor

        self.lbl_ffifo_ab_words = wx.StaticText(self, wx.ID_ANY, 'FFIFO AB Words')
        self.txt_ffifo_ab_words = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_READONLY)
        self.lbl_ffifo_cd_words = wx.StaticText(self, wx.ID_ANY, 'FFIFO CD Words')
        self.txt_ffifo_cd_words = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_READONLY)
        self.lbl_sfifo_words = wx.StaticText(self, wx.ID_ANY, 'SFIFO Words')
        self.txt_sfifo_words = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_READONLY)

        self.fifo_occupancy_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()
        self.t = threading.Thread(target=self._update_fifo_occupancy)
        self.t.start()

    def __set_properties(self):
        # no special properties
        pass

    def __do_layout(self):
        sizer_fifo_occupancy_box = wx.StaticBoxSizer(self.fifo_occupancy_box, wx.VERTICAL)

        sizer_ffifo_ab = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ffifo_ab.Add(self.lbl_ffifo_ab_words, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ffifo_ab.Add(self.txt_ffifo_ab_words, 2, wx.EXPAND, 0)

        sizer_ffifo_cd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ffifo_cd.Add(self.lbl_ffifo_cd_words, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ffifo_cd.Add(self.txt_ffifo_cd_words, 2, wx.EXPAND, 0)

        sizer_sfifo = wx.BoxSizer(wx.HORIZONTAL)
        sizer_sfifo.Add(self.lbl_sfifo_words, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_sfifo.Add(self.txt_sfifo_words, 2, wx.EXPAND, 0)

        sizer_fifo_occupancy_box.Add(sizer_ffifo_ab, 1, wx.EXPAND)
        sizer_fifo_occupancy_box.Add(sizer_ffifo_cd, 1, wx.EXPAND)
        sizer_fifo_occupancy_box.Add(sizer_sfifo, 1, wx.EXPAND)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_fifo_occupancy_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        pass

    def initialize_controls(self):
        self.txt_ffifo_ab_words.SetValue(str(self.data_processor.get_ffifo_words(self.data_processor.ChAB)))
        self.txt_ffifo_cd_words.SetValue(str(self.data_processor.get_ffifo_words(self.data_processor.ChCD)))
        self.txt_sfifo_words.SetValue(str(self.data_processor.get_sfifo_words()))

    def _update_fifo_occupancy(self):
        """
        Worker thread that checks the current FIFO occupancy and updates the values displayed in the GUI
        """
        while True:
            if self:
                self.txt_ffifo_ab_words.SetValue(str(self.data_processor.get_ffifo_words_cached(self.data_processor.ChAB)))
                self.txt_ffifo_cd_words.SetValue(str(self.data_processor.get_ffifo_words_cached(self.data_processor.ChCD)))
                self.txt_sfifo_words.SetValue(str(self.data_processor.get_sfifo_words_cached()))
                time.sleep(0.5)
            else:
                break

