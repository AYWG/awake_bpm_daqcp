# Panel for adjusting calibration gain

import wx


class CalGainPanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.btn_update_cal_gain = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_cal_gain_a = wx.StaticText(self, wx.ID_ANY, 'CAL:GAIN:A')
        self.txt_cal_gain_a = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_cal_gain_b = wx.StaticText(self, wx.ID_ANY, 'CAL:GAIN:B')
        self.txt_cal_gain_b = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_cal_gain_c = wx.StaticText(self, wx.ID_ANY, 'CAL:GAIN:C')
        self.txt_cal_gain_c = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_cal_gain_d = wx.StaticText(self, wx.ID_ANY, 'CAL:GAIN:D')
        self.txt_cal_gain_d = wx.TextCtrl(self, wx.ID_ANY, '')

        self.cal_gain_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_cal_gain_box = wx.StaticBoxSizer(self.cal_gain_box, wx.VERTICAL)

        sizer_cal_gain_a = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cal_gain_a.Add(self.lbl_cal_gain_a, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_cal_gain_a.Add(self.txt_cal_gain_a, 1, wx.EXPAND, 0)

        sizer_cal_gain_b = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cal_gain_b.Add(self.lbl_cal_gain_b, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_cal_gain_b.Add(self.txt_cal_gain_b, 1, wx.EXPAND, 0)

        sizer_cal_gain_c = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cal_gain_c.Add(self.lbl_cal_gain_c, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_cal_gain_c.Add(self.txt_cal_gain_c, 1, wx.EXPAND, 0)

        sizer_cal_gain_d = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cal_gain_d.Add(self.lbl_cal_gain_d, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_cal_gain_d.Add(self.txt_cal_gain_d, 1, wx.EXPAND, 0)

        sizer_cal_gain_box.Add(self.btn_update_cal_gain, 0, wx.EXPAND, 0)
        sizer_cal_gain_box.Add(sizer_cal_gain_a, 0, wx.ALL | wx.EXPAND, 4)
        sizer_cal_gain_box.Add(sizer_cal_gain_b, 0, wx.ALL | wx.EXPAND, 4)
        sizer_cal_gain_box.Add(sizer_cal_gain_c, 0, wx.ALL | wx.EXPAND, 4)
        sizer_cal_gain_box.Add(sizer_cal_gain_d, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_cal_gain_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)
