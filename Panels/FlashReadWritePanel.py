import wx


class FlashReadWritePanel(wx.Panel):
    """
    Panel for reading and writing to flash memory on the FPGA
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_flash_rd = wx.Button(self, wx.ID_ANY, 'Read From Flash')
        self.btn_flash_wr = wx.Button(self, wx.ID_ANY, '  Write To Flash  ')  # Added spaces to make buttons same width

        self.flash_rd_wr_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):
        # no special properties
        pass

    def __do_layout(self):
        sizer_flash_rd_wr_box = wx.StaticBoxSizer(self.flash_rd_wr_box, wx.VERTICAL)

        sizer_flash_rd_wr = wx.BoxSizer(wx.VERTICAL)
        sizer_flash_rd_wr.Add(self.btn_flash_rd, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_flash_rd_wr.Add(self.btn_flash_wr, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)

        sizer_flash_rd_wr_box.Add(sizer_flash_rd_wr, 1, wx.EXPAND, 0)
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_flash_rd_wr_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnRead, self.btn_flash_rd)
        self.Bind(wx.EVT_BUTTON, self.OnWrite, self.btn_flash_wr)

    def initialize_controls(self):
        # no initial control values (there're only 2 buttons)
        pass

    def OnRead(self, event):
        self.data_processor.rd_flash()
        # We pass the event to the parent frame (CtrlWindow) so that it can update all the
        # controls with data from the flash
        event.Skip()

    def OnWrite(self, event):
        self.data_processor.wr_flash()
        wx.MessageBox("Write to Flash Successful", "Success")
