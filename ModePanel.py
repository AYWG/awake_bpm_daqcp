# Panel for setting the BPM mode

import wx


class ModePanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
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
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):
        pass

    def __do_layout(self):
        SIZER_BORDER_WIDTH = 5
        BOX_BORDER_WIDTH = 4
        sizer_mode_box = wx.StaticBoxSizer(self.mode_box, wx.VERTICAL)

        sizer_run = wx.BoxSizer(wx.HORIZONTAL)
        sizer_run.Add(self.lbl_run, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_run.Add(self.chk_run, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_ext_trig = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ext_trig.Add(self.lbl_ext_trig, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_ext_trig.Add(self.chk_ext_trig, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_self_trig = wx.BoxSizer(wx.HORIZONTAL)
        sizer_self_trig.Add(self.lbl_self_trig, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_self_trig.Add(self.chk_self_trig, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_int_trig = wx.BoxSizer(wx.HORIZONTAL)
        sizer_int_trig.Add(self.lbl_int_trig, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_int_trig.Add(self.chk_int_trig, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_ena_trig_out = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ena_trig_out.Add(self.lbl_ena_trig_out, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_ena_trig_out.Add(self.chk_ena_trig_out, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_ena_temp_rd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ena_temp_rd.Add(self.lbl_ena_temp_rd, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_ena_temp_rd.Add(self.chk_ena_temp_rd, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_bypass_blr = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bypass_blr.Add(self.lbl_bypass_blr, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_bypass_blr.Add(self.chk_bypass_blr, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_raw_adc_rd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_raw_adc_rd.Add(self.lbl_raw_adc_rd, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_raw_adc_rd.Add(self.chk_raw_adc_rd, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_blr_rd = wx.BoxSizer(wx.HORIZONTAL)
        sizer_blr_rd.Add(self.lbl_blr_rd, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_blr_rd.Add(self.chk_blr_rd, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_afe_cal = wx.BoxSizer(wx.HORIZONTAL)
        sizer_afe_cal.Add(self.lbl_afe_cal, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_afe_cal.Add(self.chk_afe_cal, 0, ((wx.LEFT | wx.RIGHT) | wx.wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_onfly_cal = wx.BoxSizer(wx.HORIZONTAL)
        sizer_onfly_cal.Add(self.lbl_onfly_cal, 1, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_onfly_cal.Add(self.chk_onfly_cal, 0, ((wx.LEFT | wx.RIGHT) | wx.ALIGN_TOP), SIZER_BORDER_WIDTH)

        sizer_mode_box.Add(self.btn_update_mode, 1, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_mode_box.Add(sizer_run, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_ext_trig, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_self_trig, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_int_trig, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_ena_trig_out, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_ena_temp_rd, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_bypass_blr, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_raw_adc_rd, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_blr_rd, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_afe_cal, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.Add(sizer_onfly_cal, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_mode_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_mode)

    def initialize_controls(self):
        mode = self.data_processor.get_mode()

        if mode - 0x4000 >= 0:
            mode -= 0x4000
            self.chk_onfly_cal.SetValue(True)
        if mode - 0x2000 >= 0:
            mode -= 0x2000
            self.chk_afe_cal.SetValue(True)
        if mode - 0x200 >= 0:
            mode -= 0x200
            self.chk_bypass_blr.SetValue(True)
        if mode - 0x100 >= 0:
            mode -= 0x100
            self.chk_blr_rd.SetValue(True)
        if mode - 0x20 >= 0:
            mode -= 0x20
            self.chk_ena_temp_rd.SetValue(True)
        if mode - 0x18 >= 0:
            mode -= 0x18
            self.chk_ena_trig_out.SetValue(True)
        if mode - 0x4 >= 0:
            mode -= 0x4
            self.chk_int_trig.SetValue(True)
        if mode - 0x2 >= 0:
            mode -= 0x2
            self.chk_self_trig.SetValue(True)
        if mode - 0x1 >= 0:
            mode -= 0x1
            self.chk_run.SetValue(True)

        self.chk_ext_trig.SetValue(True)
        self.chk_raw_adc_rd.SetValue(True)


    def OnUpdate(self, event):
        mode = 0x0

        # The value added represents in binary the number that must be written to the control register
        # in order to enable that particular mode (same logic in LabVIEW)
        if self.chk_run.GetValue():
            mode += 0x1
        if self.chk_ext_trig.GetValue():
            mode += 0x0
        if self.chk_self_trig.GetValue():
            mode += 0x2
        if self.chk_int_trig.GetValue():
            mode += 0x4
        if self.chk_ena_trig_out.GetValue():
            mode += 0x18
        if self.chk_ena_temp_rd.GetValue():
            mode += 0x20
        if self.chk_bypass_blr.GetValue():
            mode += 0x200
        if self.chk_raw_adc_rd.GetValue():
            mode += 0x0
        if self.chk_blr_rd.GetValue():
            mode += 0x100
        if self.chk_afe_cal.GetValue():
            mode += 0x2000
        if self.chk_onfly_cal.GetValue():
            mode += 0x4000

        self.data_processor.set_mode(mode)

        wx.MessageBox("Mode successfully updated", "Update Successful")
