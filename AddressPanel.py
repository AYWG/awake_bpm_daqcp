# Panel for setting the IP and MAC addresses

import wx


class AddressPanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.btn_update_address = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_mac_address = wx.StaticText(self, wx.ID_ANY, 'MAC')
        self.txt_mac_address_0 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_mac_address_1 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_mac_address_2 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_mac_address_3 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_mac_address_4 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_mac_address_5 = wx.TextCtrl(self, wx.ID_ANY, '')

        self.lbl_ip_address = wx.StaticText(self, wx.ID_ANY, 'IP')
        self.txt_ip_address_0 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_ip_address_1 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_ip_address_2 = wx.TextCtrl(self, wx.ID_ANY, '')
        self.txt_ip_address_3 = wx.TextCtrl(self, wx.ID_ANY, '')

        self.address_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_address_box = wx.StaticBoxSizer(self.address_box, wx.VERTICAL)

        sizer_mac_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mac_address.Add(self.lbl_mac_address, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_mac_address.Add(self.txt_mac_address_0, 1, wx.EXPAND, 0)
        sizer_mac_address.Add(self.txt_mac_address_1, 1, wx.EXPAND, 0)
        sizer_mac_address.Add(self.txt_mac_address_2, 1, wx.EXPAND, 0)
        sizer_mac_address.Add(self.txt_mac_address_3, 1, wx.EXPAND, 0)
        sizer_mac_address.Add(self.txt_mac_address_4, 1, wx.EXPAND, 0)
        sizer_mac_address.Add(self.txt_mac_address_5, 1, wx.EXPAND, 0)

        sizer_ip_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ip_address.Add(self.lbl_ip_address, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ip_address.Add(self.txt_ip_address_0, 1, wx.EXPAND, 0)
        sizer_ip_address.Add(self.txt_ip_address_1, 1, wx.EXPAND, 0)
        sizer_ip_address.Add(self.txt_ip_address_2, 1, wx.EXPAND, 0)
        sizer_ip_address.Add(self.txt_ip_address_3, 1, wx.EXPAND, 0)

        sizer_address_box.Add(self.btn_update_address, 0, wx.EXPAND, 0)
        sizer_address_box.Add(sizer_mac_address, 0, wx.EXPAND, 0)
        sizer_address_box.Add(sizer_ip_address, 0, wx.EXPAND, 0)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_address_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)
