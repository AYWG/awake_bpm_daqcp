# Panel for controlling the amount of front-end attenuation

import wx


class AFECtrlPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_gain = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_1_db_vga = wx.StaticText(self, wx.ID_ANY, '-1 dB')
        self.chk_1_db_vga = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_2_db_vga = wx.StaticText(self, wx.ID_ANY, '-2 dB')
        self.chk_2_db_vga = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_4_db_vga = wx.StaticText(self, wx.ID_ANY, '-4 dB')
        self.chk_4_db_vga = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_8_db_vga = wx.StaticText(self, wx.ID_ANY, '-8 dB')
        self.chk_8_db_vga = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_16_db_vga = wx.StaticText(self, wx.ID_ANY, '-16 dB')
        self.chk_16_db_vga = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_vga_att = wx.StaticText(self, wx.ID_ANY, 'VGA-Att')

        self.lbl_1_db_digi = wx.StaticText(self, wx.ID_ANY, '-1 dB')
        self.chk_1_db_digi = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_2_db_digi = wx.StaticText(self, wx.ID_ANY, '-2 dB')
        self.chk_2_db_digi = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_4_db_digi = wx.StaticText(self, wx.ID_ANY, '-4 dB')
        self.chk_4_db_digi = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_8_db_digi = wx.StaticText(self, wx.ID_ANY, '-8 dB')
        self.chk_8_db_digi = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_16_db_digi = wx.StaticText(self, wx.ID_ANY, '-16 dB')
        self.chk_16_db_digi = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_digi_att = wx.StaticText(self, wx.ID_ANY, 'Digi-Att')

        self.afe_ctrl_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_afe_ctrl_box = wx.StaticBoxSizer(self.afe_ctrl_box, wx.VERTICAL)

        sizer_1_db_vga = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1_db_vga.Add(self.lbl_1_db_vga, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_1_db_vga.Add(self.chk_1_db_vga, 0, wx.EXPAND)

        sizer_2_db_vga = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_db_vga.Add(self.lbl_2_db_vga, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_2_db_vga.Add(self.chk_2_db_vga, 0, wx.EXPAND)

        sizer_4_db_vga = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_db_vga.Add(self.lbl_4_db_vga, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_4_db_vga.Add(self.chk_4_db_vga, 0, wx.EXPAND)

        sizer_8_db_vga = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8_db_vga.Add(self.lbl_8_db_vga, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_8_db_vga.Add(self.chk_8_db_vga, 0, wx.EXPAND)

        sizer_16_db_vga = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16_db_vga.Add(self.lbl_16_db_vga, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_16_db_vga.Add(self.chk_16_db_vga, 0, wx.EXPAND)

        sizer_vga_main = wx.BoxSizer(wx.VERTICAL)
        sizer_vga_main.Add(sizer_1_db_vga, 0, wx.ALL | wx.EXPAND, 4)
        sizer_vga_main.Add(sizer_2_db_vga, 0, wx.ALL | wx.EXPAND, 4)
        sizer_vga_main.Add(sizer_4_db_vga, 0, wx.ALL | wx.EXPAND, 4)
        sizer_vga_main.Add(sizer_8_db_vga, 0, wx.ALL | wx.EXPAND, 4)
        sizer_vga_main.Add(sizer_16_db_vga, 0, wx.ALL | wx.EXPAND, 4)
        sizer_vga_main.Add(self.lbl_vga_att, 0, wx.ALL | wx.EXPAND, 4)

        sizer_1_db_digi = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1_db_digi.Add(self.lbl_1_db_digi, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_1_db_digi.Add(self.chk_1_db_digi, 0, wx.EXPAND)

        sizer_2_db_digi = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2_db_digi.Add(self.lbl_2_db_digi, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_2_db_digi.Add(self.chk_2_db_digi, 0, wx.EXPAND)

        sizer_4_db_digi = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4_db_digi.Add(self.lbl_4_db_digi, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_4_db_digi.Add(self.chk_4_db_digi, 0, wx.EXPAND)

        sizer_8_db_digi = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8_db_digi.Add(self.lbl_8_db_digi, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_8_db_digi.Add(self.chk_8_db_digi, 0, wx.EXPAND)

        sizer_16_db_digi = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16_db_digi.Add(self.lbl_16_db_digi, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_16_db_digi.Add(self.chk_16_db_digi, 0, wx.EXPAND)

        sizer_digi_main = wx.BoxSizer(wx.VERTICAL)
        sizer_digi_main.Add(sizer_1_db_digi, 0, wx.ALL | wx.EXPAND, 4)
        sizer_digi_main.Add(sizer_2_db_digi, 0, wx.ALL | wx.EXPAND, 4)
        sizer_digi_main.Add(sizer_4_db_digi, 0, wx.ALL | wx.EXPAND, 4)
        sizer_digi_main.Add(sizer_8_db_digi, 0, wx.ALL | wx.EXPAND, 4)
        sizer_digi_main.Add(sizer_16_db_digi, 0, wx.ALL | wx.EXPAND, 4)
        sizer_digi_main.Add(self.lbl_digi_att, 0, wx.ALL | wx.EXPAND, 4)

        sizer_afe = wx.BoxSizer(wx.HORIZONTAL)
        sizer_afe.Add(sizer_digi_main, 1, wx.ALL | wx.EXPAND, 4)
        sizer_afe.Add(sizer_vga_main, 1, wx.ALL | wx.EXPAND, 4)

        sizer_afe_ctrl_box.Add(self.btn_update_gain, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_afe_ctrl_box.Add(sizer_afe, 0, wx.ALL | wx.EXPAND, 4)
        # sizer_afe_ctrl_box.Add(sizer_1_db, 0, wx.ALL | wx.EXPAND, 4)
        # sizer_afe_ctrl_box.Add(sizer_2_db, 0, wx.ALL | wx.EXPAND, 4)
        # sizer_afe_ctrl_box.Add(sizer_4_db, 0, wx.ALL | wx.EXPAND, 4)
        # sizer_afe_ctrl_box.Add(sizer_8_db, 0, wx.ALL | wx.EXPAND, 4)
        # sizer_afe_ctrl_box.Add(sizer_16_db, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_afe_ctrl_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_gain)

    def initialize_controls(self):
        gain = self.data_processor.get_afe_gain()

        if (gain - 8192 >= 0):
            gain -= 8192
            self.chk_16_db_digi.SetValue(True)
        if (gain - 4096 >= 0):
            gain -= 4096
            self.chk_8_db_digi.SetValue(True)
        if (gain - 2048 >= 0):
            gain -= 2048
            self.chk_4_db_digi.SetValue(True)
        if (gain - 1024 >= 0):
            gain -= 1024
            self.chk_2_db_digi.SetValue(True)
        if (gain - 512 >= 0):
            gain -= 512
            self.chk_1_db_digi.SetValue(True)
        if (gain - 16 >= 0):
            gain -= 16
            self.chk_16_db_vga.SetValue(True)
        if (gain - 8 >= 0):
            gain -= 8
            self.chk_8_db_vga.SetValue(True)
        if (gain - 4 >= 0):
            gain -= 4
            self.chk_4_db_vga.SetValue(True)
        if (gain - 2 >= 0):
            gain -= 2
            self.chk_2_db_vga.SetValue(True)
        if (gain - 1 >= 0):
            gain -= 1
            self.chk_1_db_vga.SetValue(True)

    def OnUpdate(self, event):
        gain = 0
        if self.chk_1_db_vga.GetValue():
            gain += 1
        if self.chk_2_db_vga.GetValue():
            gain += 2
        if self.chk_4_db_vga.GetValue():
            gain += 4
        if self.chk_8_db_vga.GetValue():
            gain += 8
        if self.chk_16_db_vga.GetValue():
            gain += 16
        if self.chk_1_db_digi.GetValue():
            gain += 512
        if self.chk_2_db_digi.GetValue():
            gain += 1024
        if self.chk_4_db_digi.GetValue():
            gain += 2048
        if self.chk_8_db_digi.GetValue():
            gain += 4096
        if self.chk_16_db_digi.GetValue():
            gain += 8192

        self.data_processor.set_afe_gain(gain)
        self.data_processor.wr_flash_buf()

        wx.MessageBox("AFE Gain successfully updated", "Update Successful")
