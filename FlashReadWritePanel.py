# Panel for reading and writing to flash memory on the FPGA

import wx


class FlashReadWritePanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_flash_rd = wx.Button(self, wx.ID_ANY, 'Read From Flash')
        self.btn_flash_wr = wx.Button(self, wx.ID_ANY, 'Write To Flash')

        self.flash_rd_wr_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_flash_rd_wr_box = wx.StaticBoxSizer(self.flash_rd_wr_box, wx.VERTICAL)

        sizer_flash_rd_wr_box.Add(self.btn_flash_rd, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_flash_rd_wr_box.Add(self.btn_flash_wr, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_flash_rd_wr_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)
