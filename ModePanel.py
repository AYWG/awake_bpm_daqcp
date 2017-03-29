# Panel for setting the BPM mode

import wx


class ModePanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.btn_update_mode = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_run = wx.StaticText(self, wx.ID_ANY, 'Run')
        self.chk_run = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_ext_trig = wx.StaticText(self, wx.ID_ANY, 'External Trigger')
        self.chk_ext_trig = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_self_trig = wx.StaticText(self, wx.ID_ANY, 'Self Trigger')
        self.chk_self_trig = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_int_trig = wx.StaticText(self, wx.ID_ANY, 'Internal Trigger')
        self.chk_int_trig = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_ena_trig_out = wx.StaticText(self, wx.ID_ANY, 'Enable Trigger Output')
        self.chk_ena_trig_out = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_ena_temp_rd = wx.StaticText(self, wx.ID_ANY, 'Enable Temperature Reading')
        self.chk_ena_temp_rd = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_bypass_blr = wx.StaticText(self, wx.ID_ANY, 'Bypass BLR')
        self.chk_bypass_blr = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_raw_adc_rd = wx.StaticText(self, wx.ID_ANY, 'RAW ADC Readout')
        self.chk_raw_adc_rd = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_blr_rd = wx.StaticText(self, wx.ID_ANY, 'BLR Readout')
        self.chk_blr_rd = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_afe_cal = wx.StaticText(self, wx.ID_ANY, 'AFE Cal.')
        self.chk_afe_cal = wx.CheckBox(self, wx.ID_ANY)
        self.lbl_onfly_cal = wx.StaticText(self, wx.ID_ANY, 'On Fly Cal.')
        self.chk_onfly_cal = wx.CheckBox(self, wx.ID_ANY)

        self.mode_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_mode_box = wx.StaticBoxSizer(self.mode_box, wx.VERTICAL)

        sizer_run = wx.BoxSizer(wx.HORIZONTAL)
        sizer_run.Add(self.lbl_run, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_run.Add(self.chk_run, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_ext_trig = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ext_trig.Add(self.lbl_ext_trig, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_ext_trig.Add(self.chk_ext_trig, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_self_trig = wx.BoxSizer(wx.HORIZONTAL)
        sizer_self_trig.Add(self.lbl_self_trig, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_self_trig.Add(self.chk_self_trig, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_int_trig = wx.BoxSizer(wx.HORIZONTAL)
        sizer_int_trig.Add(self.lbl_int_trig, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_int_trig.Add(self.chk_int_trig, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_ena_trig_out = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ena_trig_out.Add(self.lbl_ena_trig_out, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_ena_trig_out.Add(self.chk_ena_trig_out, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_ena_temp_rd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ena_temp_rd.Add(self.lbl_ena_temp_rd, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_ena_temp_rd.Add(self.chk_ena_temp_rd, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_bypass_blr = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bypass_blr.Add(self.lbl_bypass_blr, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_bypass_blr.Add(self.chk_bypass_blr, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_raw_adc_rd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_raw_adc_rd.Add(self.lbl_raw_adc_rd, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_raw_adc_rd.Add(self.chk_raw_adc_rd, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_blr_rd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_blr_rd.Add(self.lbl_blr_rd, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_blr_rd.Add(self.chk_blr_rd, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_afe_cal = wx.BoxSizer(wx.HORIZONTAL)
        sizer_afe_cal.Add(self.lbl_afe_cal, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_afe_cal.Add(self.chk_afe_cal, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_onfly_cal = wx.BoxSizer(wx.HORIZONTAL)
        sizer_onfly_cal.Add(self.lbl_onfly_cal, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), 10)
        sizer_onfly_cal.Add(self.chk_onfly_cal, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_CENTER), 10)

        sizer_mode_box.Add(self.btn_update_mode, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_mode_box.Add(sizer_run, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_ext_trig, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_self_trig, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_int_trig, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_ena_trig_out, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_ena_temp_rd, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_bypass_blr, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_raw_adc_rd, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_blr_rd, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_afe_cal, 0, wx.ALL | wx.EXPAND, 4)
        sizer_mode_box.Add(sizer_onfly_cal, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_mode_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)
