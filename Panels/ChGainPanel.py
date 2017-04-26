import string
import wx
import Validator
from Constants import Channels


class ChGainPanel(wx.Panel):
    """
    Panel for adjusting channel gain
    """

    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_ch_gain = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_ch_gain = []
        self.txt_ch_gain = []
        for i in range(4):
            self.lbl_ch_gain.append(wx.StaticText(self, wx.ID_ANY, 'CH:GAIN:' + Channels.channels[i]))
            self.txt_ch_gain.append(wx.TextCtrl(self, wx.ID_ANY, ''))

        self.ch_gain_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):
        # Associate the validator with each input
        for i in range(len(self.txt_ch_gain)): self.txt_ch_gain[i].SetValidator(ChGainValidator())

    def __do_layout(self):
        sizer_ch_gain_box = wx.StaticBoxSizer(self.ch_gain_box, wx.VERTICAL)
        sizer_ch_gain_box.Add(self.btn_update_ch_gain, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)

        sizer_ch_gain = []

        for i in range(len(self.txt_ch_gain)):
            sizer_ch_gain.append(wx.BoxSizer(wx.HORIZONTAL))
            sizer_ch_gain[i].Add(self.lbl_ch_gain[i], 1, wx.ALL | wx.ALIGN_CENTER, 4)
            sizer_ch_gain[i].Add(self.txt_ch_gain[i], 2, wx.EXPAND, 0)
            sizer_ch_gain_box.Add(sizer_ch_gain[i], 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_ch_gain_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_ch_gain)

    def initialize_controls(self):
        """
        Initialize the ch gain panel with values from the FPGA
        """
        for i in range(len(self.txt_ch_gain)):
            ch_gain = self.data_processor.int_to_float(self.data_processor.get_ch_gain(Channels.channels[i]))
            self.txt_ch_gain[i].SetValue(str(ch_gain))

    def OnUpdate(self, event):
        if self.Validate():
            for i in range(len(self.txt_ch_gain)):
                # Everything is validated, so convert the inputs to floats
                ch_gain = float(self.txt_ch_gain[i].GetValue())
                # We then need to convert the values to the IEEE 754 representation as integers
                ch_gain = self.data_processor.float_to_int(ch_gain)
                # Load the relevant data to the FPGA
                self.data_processor.set_ch_gain(Channels.channels[i], ch_gain)

            wx.MessageBox("Ch Gain successfully updated", "Success")


class ChGainValidator(Validator.Validator):
    """
    Validator subclass for validating ch gain inputs
    """

    def __init__(self):
        Validator.Validator.__init__(self)

    def Clone(self):
        return ChGainValidator()

    def Validate(self, parent):
        textCtrl = self.GetWindow()
        val = textCtrl.GetValue()
        gain_upper_limit = 5.0
        gain_lower_limit = -5.0

        if len(val) == 0:
            wx.MessageBox("Ch Gain value required!", "No Input")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        elif not ChGainValidator.is_float(val):
            wx.MessageBox("Please enter a valid decimal value", "Invalid Input")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        elif float(val) > gain_upper_limit or float(val) < gain_lower_limit:
            wx.MessageBox("Please enter a value that is within the accepted range (+/- " + str(gain_upper_limit) + ")", "Out of Range")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if chr(key) in string.digits or chr(key) == '.' or chr(key) == '-':
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
        return
