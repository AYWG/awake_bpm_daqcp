# Panel for setting the IP and MAC addresses

import wx

HEX_ONLY = 1
DIGIT_ONLY = 2


class AddressPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_address = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_mac_address = wx.StaticText(self, wx.ID_ANY, 'MAC')
        self.txt_mac_address_0 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        self.txt_mac_address_1 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        self.txt_mac_address_2 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        self.txt_mac_address_3 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        self.txt_mac_address_4 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        self.txt_mac_address_5 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))

        self.lbl_ip_address = wx.StaticText(self, wx.ID_ANY, 'IP')
        self.txt_ip_address_0 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))
        self.txt_ip_address_1 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))
        self.txt_ip_address_2 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))
        self.txt_ip_address_3 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))

        self.address_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()

    def __set_properties(self):
        pass

    def __do_layout(self):
        SIZER_BORDER_WIDTH = 5
        BOX_BORDER_WIDTH = 5

        sizer_address_box = wx.StaticBoxSizer(self.address_box, wx.VERTICAL)

        sizer_mac_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mac_address.Add(self.lbl_mac_address, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_mac_address.Add(self.txt_mac_address_0, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_mac_address.Add(self.txt_mac_address_1, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_mac_address.Add(self.txt_mac_address_2, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_mac_address.Add(self.txt_mac_address_3, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_mac_address.Add(self.txt_mac_address_4, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_mac_address.Add(self.txt_mac_address_5, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)

        sizer_ip_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ip_address.Add(self.lbl_ip_address, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ip_address.Add(self.txt_ip_address_0, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_ip_address.Add(self.txt_ip_address_1, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_ip_address.Add(self.txt_ip_address_2, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)
        sizer_ip_address.Add(self.txt_ip_address_3, 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)

        sizer_address_box.Add(self.btn_update_address, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_address_box.Add(sizer_mac_address, 0, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)
        sizer_address_box.Add(sizer_ip_address, 0, wx.ALL | wx.EXPAND, BOX_BORDER_WIDTH)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_address_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_address)

    def OnUpdate(self, event):
        pass


class AddressValidator(wx.PyValidator):
    def __init__(self, flag=None):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return AddressValidator(self.flag)

    def Validate(self, parent):
        textCtrl = self.GetWindow()
        val = textCtrl.GetValue()

        # if self.flag == HEX_ONLY:

        # elif self.flag == DIGIT_ONLY:

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True



