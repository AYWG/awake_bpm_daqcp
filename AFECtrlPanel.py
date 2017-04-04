# Panel for controlling the amount of front-end attenuation

import wx


class AFECtrlPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_gain = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_1_db = wx.StaticText(self, wx.ID_ANY, '-1 dB')
        self.chk_1_db = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_2_db = wx.StaticText(self, wx.ID_ANY, '-2 dB')
        self.chk_2_db = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_4_db = wx.StaticText(self, wx.ID_ANY, '-4 dB')
        self.chk_4_db = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_8_db = wx.StaticText(self, wx.ID_ANY, '-8 dB')
        self.chk_8_db = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_16_db = wx.StaticText(self, wx.ID_ANY, '-16 dB')
        self.chk_16_db = wx.CheckBox(self, wx.ID_ANY)

        self.afe_ctrl_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_afe_ctrl_box = wx.StaticBoxSizer(self.afe_ctrl_box, wx.VERTICAL)

        sizer_1_db = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1_db.Add(self.lbl_1_db, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_1_db.Add(self.chk_1_db, 0, wx.EXPAND)

        sizer_2_db = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_db.Add(self.lbl_2_db, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_2_db.Add(self.chk_2_db, 0, wx.EXPAND)

        sizer_4_db = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_db.Add(self.lbl_4_db, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_4_db.Add(self.chk_4_db, 0, wx.EXPAND)

        sizer_8_db = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8_db.Add(self.lbl_8_db, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_8_db.Add(self.chk_8_db, 0, wx.EXPAND)

        sizer_16_db = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16_db.Add(self.lbl_16_db, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_16_db.Add(self.chk_16_db, 0, wx.EXPAND)

        sizer_afe_ctrl_box.Add(self.btn_update_gain, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_afe_ctrl_box.Add(sizer_1_db, 0, wx.ALL | wx.EXPAND, 4)
        sizer_afe_ctrl_box.Add(sizer_2_db, 0, wx.ALL | wx.EXPAND, 4)
        sizer_afe_ctrl_box.Add(sizer_4_db, 0, wx.ALL | wx.EXPAND, 4)
        sizer_afe_ctrl_box.Add(sizer_8_db, 0, wx.ALL | wx.EXPAND, 4)
        sizer_afe_ctrl_box.Add(sizer_16_db, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_afe_ctrl_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_gain)

    def OnUpdate(self, event):
        gain = 0
        if self.chk_1_db.GetValue():
            gain += 1
        if self.chk_2_db.GetValue():
            gain += 2
        if self.chk_4_db.GetValue():
            gain += 4
        if self.chk_8_db.GetValue():
            gain += 8
        if self.chk_16_db.GetValue():
            gain += 16

        self.data_processor.set_afe_gain(gain)
        self.data_processor.wr_flash_buf()
