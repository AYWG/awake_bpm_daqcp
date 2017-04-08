import wx
import string
import Validator

HEX_ONLY = 1
DIGIT_ONLY = 2


class AddressPanel(wx.Panel):
    """
    Panel for setting the IP and MAC address of the BPM
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_address = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_mac_address = wx.StaticText(self, wx.ID_ANY, 'MAC')

        # MAC address is made up of 6 components
        self.txt_mac_address = []
        for _ in range(6): self.txt_mac_address.append(wx.TextCtrl(self, wx.ID_ANY, '', size=(30, -1)))

        # IP address is made up of 4 components
        self.txt_ip_address = []
        for _ in range(4): self.txt_ip_address.append(wx.TextCtrl(self, wx.ID_ANY, '', size=(40, -1)))

        self.lbl_ip_address = wx.StaticText(self, wx.ID_ANY, 'IP')

        self.address_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):

        for i in range(len(self.txt_mac_address)):
            # Each portion of the MAC address is 2 characters
            self.txt_mac_address[i].SetMaxLength(2)
            # Only hexadecimals are allowed
            self.txt_mac_address[i].SetValidator(AddressValidator(HEX_ONLY))

        for i in range(len(self.txt_ip_address)):
            # Each portion of the IP address is at most 3 characters
            self.txt_ip_address[i].SetMaxLength(3)
            # Only digits are allowed
            self.txt_ip_address[i].SetValidator(AddressValidator(DIGIT_ONLY))

    def __do_layout(self):
        SIZER_BORDER_WIDTH = 5
        BOX_BORDER_WIDTH = 5

        sizer_address_box = wx.StaticBoxSizer(self.address_box, wx.VERTICAL)

        sizer_mac_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mac_address.Add(self.lbl_mac_address, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        for i in range(len(self.txt_mac_address)):
            sizer_mac_address.Add(self.txt_mac_address[i], 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)

        sizer_ip_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ip_address.Add(self.lbl_ip_address, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        for i in range(len(self.txt_ip_address)):
            sizer_ip_address.Add(self.txt_ip_address[i], 0, ((wx.LEFT | wx.RIGHT) | wx.EXPAND), SIZER_BORDER_WIDTH)

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
        """
        Writes the current MAC/IP address (stored in the BPM's flash buffer) to the appropriate TextCtrl boxes.
        """

        for i in range(len(self.txt_mac_address)):
            self.txt_mac_address[i].SetValue(format(self.data_processor.get_mac_address(i), 'x'))

        self._format_mac_address()

        for i in range(len(self.txt_ip_address)):
            self.txt_ip_address[i].SetValue(str(self.data_processor.get_ip_address(i)))

    def OnUpdate(self, event):
        """

        :param event:
        :return:
        """
        if self.Validate():

            for i in range(len(self.txt_mac_address)):
                self.data_processor.set_mac_address(i, int(self.txt_mac_address[i].GetValue(), 16))

            self._format_mac_address()

            for i in range(len(self.txt_ip_address)):
                self.data_processor.set_ip_address(i, int(self.txt_ip_address[i].GetValue()))

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
                textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
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
