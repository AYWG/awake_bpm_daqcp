# Panel for setting the IP and MAC addresses

import wx
import string
import Validator

HEX_ONLY = 1
DIGIT_ONLY = 2


class AddressPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_address = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_mac_address = wx.StaticText(self, wx.ID_ANY, 'MAC')

        self.txt_mac_address = []
        for _ in range(6): self.txt_mac_address.append(wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1)))
        # self.txt_mac_address_0 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        # self.txt_mac_address_1 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        # self.txt_mac_address_2 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        # self.txt_mac_address_3 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        # self.txt_mac_address_4 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))
        # self.txt_mac_address_5 = wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1))

        self.txt_ip_address = []
        for _ in range(4): self.txt_ip_address.append(wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1)))

        # self.lbl_ip_address = wx.StaticText(self, wx.ID_ANY, 'IP')
        # self.txt_ip_address_0 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))
        # self.txt_ip_address_1 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))
        # self.txt_ip_address_2 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))
        # self.txt_ip_address_3 = wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1))

        self.address_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):

        for i in range(len(self.txt_mac_address)):
            # Each portion of the MAC address is 2 characters
            self.txt_mac_address[i].SetMaxLength(2)
            # Only hexadecimal are allowed
            self.txt_mac_address[i].SetValidator(AddressValidator(HEX_ONLY))

        # self.txt_mac_address_0.SetMaxLength(2)
        # self.txt_mac_address_1.SetMaxLength(2)
        # self.txt_mac_address_2.SetMaxLength(2)
        # self.txt_mac_address_3.SetMaxLength(2)
        # self.txt_mac_address_4.SetMaxLength(2)
        # self.txt_mac_address_5.SetMaxLength(2)

        for i in range(len(self.txt_ip_address)):
            # Each portion of the IP address is at most 3 characters
            self.txt_ip_address[i].SetMaxLength(3)
            # Only digits are allowed
            self.txt_ip_address[i].SetValidator(AddressValidator(DIGIT_ONLY))
        # self.txt_ip_address_0.SetMaxLength(3)
        # self.txt_ip_address_0.SetMaxLength(3)
        # self.txt_ip_address_0.SetMaxLength(3)
        # self.txt_ip_address_0.SetMaxLength(3)


        # self.txt_mac_address_0.SetValidator(AddressValidator(HEX_ONLY))
        # self.txt_mac_address_1.SetValidator(AddressValidator(HEX_ONLY))
        # self.txt_mac_address_2.SetValidator(AddressValidator(HEX_ONLY))
        # self.txt_mac_address_3.SetValidator(AddressValidator(HEX_ONLY))
        # self.txt_mac_address_4.SetValidator(AddressValidator(HEX_ONLY))
        # self.txt_mac_address_5.SetValidator(AddressValidator(HEX_ONLY))

        # self.txt_ip_address_0.SetValidator(AddressValidator(DIGIT_ONLY))
        # self.txt_ip_address_1.SetValidator(AddressValidator(DIGIT_ONLY))
        # self.txt_ip_address_2.SetValidator(AddressValidator(DIGIT_ONLY))
        # self.txt_ip_address_3.SetValidator(AddressValidator(DIGIT_ONLY))

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

    def initialize_controls(self):
        for i in range(len(self.txt_mac_address)):
            self.txt_mac_address[i].SetValue(format(self.data_processor.get_mac_address(i), 'x'))
        # mac_address_0 = format(self.data_processor.get_mac_address(0), 'x')
        # mac_address_1 = format(self.data_processor.get_mac_address(1), 'x')
        # mac_address_2 = format(self.data_processor.get_mac_address(2), 'x')
        # mac_address_3 = format(self.data_processor.get_mac_address(3), 'x')
        # mac_address_4 = format(self.data_processor.get_mac_address(4), 'x')
        # mac_address_5 = format(self.data_processor.get_mac_address(5), 'x')


        # if self.data_processor.get_mac_address(0) < 0x10:
        #     mac_address_0 = '0' + mac_address_0
        #
        # if self.data_processor.get_mac_address(1) < 0x10:
        #     mac_address_1 = '0' + mac_address_1
        #
        # if self.data_processor.get_mac_address(2) < 0x10:
        #     mac_address_2 = '0' + mac_address_2
        #
        # if self.data_processor.get_mac_address(3) < 0x10:
        #     mac_address_3 = '0' + mac_address_3
        #
        # if self.data_processor.get_mac_address(4) < 0x10:
        #     mac_address_4 = '0' + mac_address_4
        #
        # if self.data_processor.get_mac_address(5) < 0x10:
        #     mac_address_5 = '0' + mac_address_5



        # self.txt_mac_address_0.SetValue(mac_address_0)
        # self.txt_mac_address_1.SetValue(mac_address_1)
        # self.txt_mac_address_2.SetValue(mac_address_2)
        # self.txt_mac_address_3.SetValue(mac_address_3)
        # self.txt_mac_address_4.SetValue(mac_address_4)
        # self.txt_mac_address_5.SetValue(mac_address_5)

        self._format_mac_address()

        for i in range(len(self.txt_ip_address)):
            self.txt_ip_address[i].SetValue(str(self.data_processor.get_ip_address(i)))

        # self.txt_ip_address_0.SetValue(str(self.data_processor.get_ip_address(0)))
        # self.txt_ip_address_1.SetValue(str(self.data_processor.get_ip_address(1)))
        # self.txt_ip_address_2.SetValue(str(self.data_processor.get_ip_address(2)))
        # self.txt_ip_address_3.SetValue(str(self.data_processor.get_ip_address(3)))

    def OnUpdate(self, event):
        if self.Validate():

            for i in range(len(self.txt_mac_address)):
                self.data_processor.set_mac_address(i, int(self.txt_mac_address[i].GetValue(), 16))

            self._format_mac_address()

            for i in range(len(self.txt_ip_address)):
                self.data_processor.set_ip_address(i, int(self.txt_ip_address[i].GetValue()))
            # mac_address_0 = int(self.txt_mac_address_0.GetValue(), 16)
            # mac_address_1 = int(self.txt_mac_address_1.GetValue(), 16)
            # mac_address_2 = int(self.txt_mac_address_2.GetValue(), 16)
            # mac_address_3 = int(self.txt_mac_address_3.GetValue(), 16)
            # mac_address_4 = int(self.txt_mac_address_4.GetValue(), 16)
            # mac_address_5 = int(self.txt_mac_address_5.GetValue(), 16)

            # ip_address_0 = int(self.txt_ip_address_0.GetValue())
            # ip_address_1 = int(self.txt_ip_address_1.GetValue())
            # ip_address_2 = int(self.txt_ip_address_2.GetValue())
            # ip_address_3 = int(self.txt_ip_address_3.GetValue())

            # self.data_processor.set_mac_address(0, mac_address_0)
            # self.data_processor.set_mac_address(1, mac_address_1)
            # self.data_processor.set_mac_address(2, mac_address_2)
            # self.data_processor.set_mac_address(3, mac_address_3)
            # self.data_processor.set_mac_address(4, mac_address_4)
            # self.data_processor.set_mac_address(5, mac_address_5)

            # self._format_mac_address()

            # self.data_processor.set_ip_address(0, ip_address_0)
            # self.data_processor.set_ip_address(1, ip_address_1)
            # self.data_processor.set_ip_address(2, ip_address_2)
            # self.data_processor.set_ip_address(3, ip_address_3)

            wx.MessageBox("Addresses successfully updated", "Update Successful")

    def _format_mac_address(self):
        """
        Formats the values currently in the MAC address text boxes to be 2-character hex strings.
        :return:
        """
        mac_address = []

        for i in range(len(self.txt_mac_address)):
            mac_address.append(self.txt_mac_address[i].GetValue().upper())
            if int(mac_address[i], 16) < 0x10 and len(mac_address[i]) == 1:
                mac_address[i] = '0' + mac_address[i]
            self.txt_mac_address[i].SetValue(mac_address[i])


        # mac_address_0 = self.txt_mac_address_0.GetValue().upper()
        # mac_address_1 = self.txt_mac_address_1.GetValue().upper()
        # mac_address_2 = self.txt_mac_address_2.GetValue().upper()
        # mac_address_3 = self.txt_mac_address_3.GetValue().upper()
        # mac_address_4 = self.txt_mac_address_4.GetValue().upper()
        # mac_address_5 = self.txt_mac_address_5.GetValue().upper()

        # if int(mac_address_0, 16) < 0x10:
        #     mac_address_0 = '0' + mac_address_0
        #
        # if int(mac_address_1, 16) < 0x10:
        #     mac_address_1 = '0' + mac_address_1
        #
        # if int(mac_address_2, 16) < 0x10:
        #     mac_address_2 = '0' + mac_address_2
        #
        # if int(mac_address_3, 16) < 0x10:
        #     mac_address_3 = '0' + mac_address_3
        #
        # if int(mac_address_4, 16) < 0x10:
        #     mac_address_4 = '0' + mac_address_4
        #
        # if int(mac_address_5, 16) < 0x10:
        #     mac_address_5 = '0' + mac_address_5

        # self.txt_mac_address_0.SetValue(mac_address_0)
        # self.txt_mac_address_1.SetValue(mac_address_1)
        # self.txt_mac_address_2.SetValue(mac_address_2)
        # self.txt_mac_address_3.SetValue(mac_address_3)
        # self.txt_mac_address_4.SetValue(mac_address_4)
        # self.txt_mac_address_5.SetValue(mac_address_5)


class AddressValidator(Validator.Validator):
    def __init__(self, flag):
        Validator.Validator.__init__(self)
        self.flag = flag

    def Clone(self):
        return AddressValidator(self.flag)

    def Validate(self, parent):
        textCtrl = self.GetWindow()
        val = textCtrl.GetValue()

        # for MAC address
        if self.flag == HEX_ONLY:
            if len(val) == 0:
                wx.MessageBox("Part of the MAC address is missing!", "Missing Input")
                textCtrl.SetBackgroundColour("pink")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                return False
            elif not AddressValidator.contains_only_hex(val):
                wx.MessageBox("A MAC address may only contain hexadecimal characters", "Invalid Input")
                textCtrl.SetBackgroundColour("pink")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                return False
            else:
                textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                textCtrl.Refresh()
                return True

        # for IP address
        elif self.flag == DIGIT_ONLY:
            if len(val) == 0:
                wx.MessageBox("Part of the IP address is missing!", "Missing Input")
                textCtrl.SetBackgroundColour("pink")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                return False
            elif not AddressValidator.contains_only_digits(val):
                wx.MessageBox("An IP address may only contain numbers", "Invalid Input")
                textCtrl.SetBackgroundColour("pink")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                return False
            elif int(val) > 255:
                wx.MessageBox("Invalid value for an IP address (valid range is 0-255)", "Invalid Input")
                textCtrl.SetBackgroundColour("pink")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                return False
            else:
                # Add a success message here
                textCtrl.SetBackgroundColour(
                    wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                textCtrl.Refresh()
                return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if self.flag == HEX_ONLY and chr(key) in string.hexdigits:
            event.Skip()
            return

        if self.flag == DIGIT_ONLY and chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        return
