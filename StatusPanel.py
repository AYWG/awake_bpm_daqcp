import wx
# import  wx.lib.scrolledpanel as scrolled
import LED

# LED states
OFF = 0
ON = 1


class StatusPanel(wx.Panel):
# class StatusPanel(scrolled.ScrolledPanel):
    """
    Panel for showing what settings are currently enabled (akin to the LED indicators in the LabVIEW GUI)
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, name=title)
        # scrolled.ScrolledPanel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_status = wx.Button(self, wx.ID_ANY, 'Update')

        self.lbl_mode_LEDs = wx.StaticText(self, wx.ID_ANY, 'MODE REGISTER')
        self.lbl_afe_ctrl_LEDs = wx.StaticText(self, wx.ID_ANY, 'AFE CTRL REGISTER')
        self.lbl_status_LEDs = wx.StaticText(self, wx.ID_ANY, 'STATUS REGISTER')

        # List of LEDs for Mode Register, AFE Control Register, and Status
        self.mode_LEDs = []
        self.afe_ctrl_LEDs = []
        self.status_LEDs = []

        for _ in range(16):
            self.mode_LEDs.append(LED.LED(self))
            self.afe_ctrl_LEDs.append(LED.LED(self))
            self.status_LEDs.append(LED.LED(self))

        self.status_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()
        # self.SetupScrolling()

    def __set_properties(self):
        pass

    def __do_layout(self):
        BOX_BORDER_WIDTH = 4

        sizer_status_box = wx.StaticBoxSizer(self.status_box, wx.VERTICAL)

        # MODE REGISTER
        sizer_mode_LED_box = wx.BoxSizer(wx.HORIZONTAL)
        mode_LED_sizers = []
        for i in range(len(self.mode_LEDs)):
            mode_LED_sizers.append(wx.BoxSizer(wx.VERTICAL))
            mode_LED_sizers[i].Add(self.mode_LEDs[i], 1, wx.ALIGN_CENTER | wx.SHAPED, 0)
            mode_LED_sizers[i].Add(wx.StaticText(self, wx.ID_ANY, str(i)), 1, wx.ALIGN_CENTER | wx.SHAPED, 0)
            sizer_mode_LED_box.Add(mode_LED_sizers[i], 1, wx.EXPAND, 0)

        sizer_mode_box = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mode_box.Add(self.lbl_mode_LEDs, 0, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_mode_box.AddSpacer(19) # Add space so that LEDs line up with the rest
        sizer_mode_box.Add(sizer_mode_LED_box, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)

        # AFE CONTROL REGISTER
        sizer_afe_ctrl_LED_box = wx.BoxSizer(wx.HORIZONTAL)
        afe_ctrl_LED_sizers = []
        for i in range(len(self.afe_ctrl_LEDs)):
            afe_ctrl_LED_sizers.append(wx.BoxSizer(wx.VERTICAL))
            afe_ctrl_LED_sizers[i].Add(self.afe_ctrl_LEDs[i], 1, wx.ALIGN_CENTER | wx.SHAPED, 0)
            afe_ctrl_LED_sizers[i].Add(wx.StaticText(self, wx.ID_ANY, str(i)), 1, wx.ALIGN_CENTER | wx.SHAPED, 0)
            sizer_afe_ctrl_LED_box.Add(afe_ctrl_LED_sizers[i], 1, wx.EXPAND, 0)

        sizer_afe_ctrl_box = wx.BoxSizer(wx.HORIZONTAL)
        sizer_afe_ctrl_box.Add(self.lbl_afe_ctrl_LEDs, 0, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_afe_ctrl_box.Add(sizer_afe_ctrl_LED_box, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)

        # STATUS REGISTER
        sizer_status_LED_box = wx.BoxSizer(wx.HORIZONTAL)
        status_LED_sizers = []
        for i in range(len(self.status_LEDs)):
            status_LED_sizers.append(wx.BoxSizer(wx.VERTICAL))
            status_LED_sizers[i].Add(self.status_LEDs[i], 1, wx.ALIGN_CENTER | wx.SHAPED, 0)
            status_LED_sizers[i].Add(wx.StaticText(self, wx.ID_ANY, str(i)), 1, wx.ALIGN_CENTER | wx.SHAPED, 0)
            sizer_status_LED_box.Add(status_LED_sizers[i], 1, wx.EXPAND, 0)

        sizer_status_reg_box = wx.BoxSizer(wx.HORIZONTAL)
        sizer_status_reg_box.Add(self.lbl_status_LEDs, 0, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_status_reg_box.AddSpacer(9)
        sizer_status_reg_box.Add(sizer_status_LED_box, 1, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)

        sizer_status_box.Add(self.btn_update_status, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_status_box.Add(sizer_mode_box, 1, wx.EXPAND, 0)
        sizer_status_box.Add(sizer_afe_ctrl_box, 1, wx.EXPAND, 0)
        sizer_status_box.Add(sizer_status_reg_box, 1, wx.EXPAND, 0)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_status_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_status)

    def initialize_controls(self):
        # Read Mode, AFE Control, and Status Registers
        self._clear_LEDs()
        self._update_mode_LEDs()
        self._update_afe_ctrl_LEDs()
        self._update_status_LEDs()

    def _clear_LEDs(self):
        for i in range(len(self.mode_LEDs)):
            self.mode_LEDs[i].SetState(OFF)
            self.afe_ctrl_LEDs[i].SetState(OFF)
            self.status_LEDs[i].SetState(OFF)

    def _update_mode_LEDs(self):
        mode = self.data_processor.get_mode()

        # On Fly Cal.
        if mode - 0x4000 >= 0:
            mode -= 0x4000
            self.mode_LEDs[14].SetState(ON)
        # AFE Cal.
        if mode - 0x2000 >= 0:
            mode -= 0x2000
            self.mode_LEDs[13].SetState(ON)
        # Bypass BLR
        if mode - 0x200 >= 0:
            mode -= 0x200
            self.mode_LEDs[9].SetState(ON)
        # BLR Readout
        if mode - 0x100 >= 0:
            mode -= 0x100
            self.mode_LEDs[8].SetState(ON)
        # Ena Temp Reading
        if mode - 0x20 >= 0:
            mode -= 0x20
            self.mode_LEDs[5].SetState(ON)
        # Ena Trig Output
        if mode - 0x18 >= 0:
            mode -= 0x18
            self.mode_LEDs[4].SetState(ON)
            self.mode_LEDs[3].SetState(ON)
        # Internal Trig
        if mode - 0x4 >= 0:
            mode -= 0x4
            self.mode_LEDs[2].SetState(ON)
        # Self Trig
        if mode - 0x2 >= 0:
            mode -= 0x2
            self.mode_LEDs[1].SetState(ON)
        # Run
        if mode - 0x1 >= 0:
            mode -= 0x1
            self.mode_LEDs[0].SetState(ON)

    def _update_afe_ctrl_LEDs(self):
        gain = self.data_processor.get_afe_gain()

        for i in range(13, 8, -1):
            if gain - (1 << i) >= 0:
                gain -= 1 << i
                self.afe_ctrl_LEDs[i].SetState(ON)

        for i in range(4, -1, -1):
            if gain - (1 << i) >= 0:
                gain -= 1 << i
                self.afe_ctrl_LEDs[i].SetState(ON)

    def _update_status_LEDs(self):
        status = self.data_processor.get_status()

        for i in range(len(self.status_LEDs), -1, -1):
            if status - (1 << i) >= 0:
                status -= 1 << i
                self.status_LEDs[i].SetState(ON)

    def OnUpdate(self, event):
        self.initialize_controls()
        wx.MessageBox("Status successfully updated", "Success")