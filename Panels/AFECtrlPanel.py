import wx


class AFECtrlPanel(wx.Panel):
    """
    Panel for controlling the amount of front-end attenuation
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_gain = wx.Button(self, wx.ID_ANY, 'Update')

        self.lbl_db_vga = []
        self.chk_db_vga = []
        self.lbl_db_digi = []
        self.chk_db_digi = []

        # 5 pairs of labels and check boxes for both VGA and Digi
        for i in range(5):
            self.lbl_db_vga.append(wx.StaticText(self, wx.ID_ANY, '-' + str(1 << i) + ' dB'))
            self.lbl_db_digi.append(wx.StaticText(self, wx.ID_ANY, '-' + str(1 << i) + ' dB'))

            self.chk_db_vga.append(wx.CheckBox(self, wx.ID_ANY))
            self.chk_db_digi.append(wx.CheckBox(self, wx.ID_ANY))

        self.lbl_vga_att = wx.StaticText(self, wx.ID_ANY, 'VGA-Att')
        self.lbl_digi_att = wx.StaticText(self, wx.ID_ANY, 'Digi-Att')

        self.afe_ctrl_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):
        # no special properties
        pass

    def __do_layout(self):
        SIZER_WIDTH = 4

        sizer_afe_ctrl_box = wx.StaticBoxSizer(self.afe_ctrl_box, wx.VERTICAL)

        sizer_db_vga = []
        sizer_vga_main = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(self.chk_db_vga)):
            sizer_db_vga.append(wx.BoxSizer(wx.HORIZONTAL))
            sizer_db_vga[i].Add(self.lbl_db_vga[i], 1, wx.ALL | wx.ALIGN_CENTER, SIZER_WIDTH)
            sizer_db_vga[i].Add(self.chk_db_vga[i], 0, wx.EXPAND)
            sizer_vga_main.Add(sizer_db_vga[i], 0, wx.ALL | wx.EXPAND, SIZER_WIDTH)
        sizer_vga_main.Add(self.lbl_vga_att, 0, wx.ALL | wx.EXPAND, SIZER_WIDTH)

        sizer_db_digi = []
        sizer_digi_main = wx.BoxSizer(wx.VERTICAL)
        for i in range(len(self.chk_db_digi)):
            sizer_db_digi.append(wx.BoxSizer(wx.HORIZONTAL))
            sizer_db_digi[i].Add(self.lbl_db_digi[i], 1, wx.ALL | wx.ALIGN_CENTER, SIZER_WIDTH)
            sizer_db_digi[i].Add(self.chk_db_digi[i], 0, wx.EXPAND)
            sizer_digi_main.Add(sizer_db_digi[i], 0, wx.ALL | wx.EXPAND, SIZER_WIDTH)
        sizer_digi_main.Add(self.lbl_digi_att, 0, wx.ALL | wx.EXPAND, SIZER_WIDTH)

        sizer_afe = wx.BoxSizer(wx.HORIZONTAL)
        sizer_afe.Add(sizer_digi_main, 1, wx.ALL | wx.EXPAND, SIZER_WIDTH)
        sizer_afe.Add(sizer_vga_main, 1, wx.ALL | wx.EXPAND, SIZER_WIDTH)

        sizer_afe_ctrl_box.Add(self.btn_update_gain, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_afe_ctrl_box.Add(sizer_afe, 0, wx.ALL | wx.EXPAND, SIZER_WIDTH)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_afe_ctrl_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_gain)

    def initialize_controls(self):
        """
        Initialize the AFE Control Register Panel with values from the FPGA
        """
        gain = self.data_processor.get_afe_gain()

        # In order to determine which check boxes to set, we take the given register value
        # and work "backwards" from the value of the most significant bit to the least significant bit of the register.
        # E.g. the same logic can be used to determine that the value 135 is made up of 128 + 4 + 2 + 1
        # For the AFE Control Register, only bits 0-4 and 9-13 are used.
        for i in range(13, 8, -1):
            if gain - (1 << i) >= 0:
                gain -= 1 << i
                self.chk_db_digi[i - 9].SetValue(True)

        for i in range(4, -1, -1):
            if gain - (1 << i) >= 0:
                gain -= 1 << i
                self.chk_db_vga[i].SetValue(True)

    def OnUpdate(self, event):
        """
        When update button is clicked, the total gain represented by the checkboxes is written to the
        appropriate FPGA register as well as the flash buffer.
        """
        # Each check box corresponds to a certain value that needs to be written to the FPGA's register
        gain = 0
        for i in range(len(self.chk_db_vga)):
            if self.chk_db_vga[i].GetValue():
                gain += 1 << i

        for i in range(len(self.chk_db_digi)):
            if self.chk_db_digi[i].GetValue():
                gain += 1 << (9 + i)

        self.data_processor.set_afe_gain(gain)

        wx.MessageBox("AFE Gain successfully updated", "Success")
