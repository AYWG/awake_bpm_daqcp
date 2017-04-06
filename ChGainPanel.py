# Panel for adjusting channel gain

import wx
import string
import Validator

class ChGainPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_ch_gain = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_ch_gain_a = wx.StaticText(self, wx.ID_ANY, 'CH:GAIN:A')
        self.txt_ch_gain_a = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_ch_gain_b = wx.StaticText(self, wx.ID_ANY, 'CH:GAIN:B')
        self.txt_ch_gain_b = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_ch_gain_c = wx.StaticText(self, wx.ID_ANY, 'CH:GAIN:C')
        self.txt_ch_gain_c = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_ch_gain_d = wx.StaticText(self, wx.ID_ANY, 'CH:GAIN:D')
        self.txt_ch_gain_d = wx.TextCtrl(self, wx.ID_ANY, '')

        self.ch_gain_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()
        self.initialize_controls()

    def __set_properties(self):
        self.txt_ch_gain_a.SetValidator(ChGainValidator())
        self.txt_ch_gain_b.SetValidator(ChGainValidator())
        self.txt_ch_gain_c.SetValidator(ChGainValidator())
        self.txt_ch_gain_d.SetValidator(ChGainValidator())

    def __do_layout(self):
        sizer_ch_gain_box = wx.StaticBoxSizer(self.ch_gain_box, wx.VERTICAL)

        sizer_ch_gain_a = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ch_gain_a.Add(self.lbl_ch_gain_a, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ch_gain_a.Add(self.txt_ch_gain_a, 2, wx.EXPAND, 0)

        sizer_ch_gain_b = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ch_gain_b.Add(self.lbl_ch_gain_b, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ch_gain_b.Add(self.txt_ch_gain_b, 2, wx.EXPAND, 0)

        sizer_ch_gain_c = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ch_gain_c.Add(self.lbl_ch_gain_c, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ch_gain_c.Add(self.txt_ch_gain_c, 2, wx.EXPAND, 0)

        sizer_ch_gain_d = wx.BoxSizer(wx.HORIZONTAL)
        sizer_ch_gain_d.Add(self.lbl_ch_gain_d, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_ch_gain_d.Add(self.txt_ch_gain_d, 2, wx.EXPAND, 0)

        sizer_ch_gain_box.Add(self.btn_update_ch_gain, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_ch_gain_box.Add(sizer_ch_gain_a, 0, wx.ALL | wx.EXPAND, 4)
        sizer_ch_gain_box.Add(sizer_ch_gain_b, 0, wx.ALL | wx.EXPAND, 4)
        sizer_ch_gain_box.Add(sizer_ch_gain_c, 0, wx.ALL | wx.EXPAND, 4)
        sizer_ch_gain_box.Add(sizer_ch_gain_d, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_ch_gain_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_ch_gain)

    def initialize_controls(self):
        ch_gain_a = self.data_processor.int_to_float(self.data_processor.get_ch_gain_a())
        ch_gain_b = self.data_processor.int_to_float(self.data_processor.get_ch_gain_b())
        ch_gain_c = self.data_processor.int_to_float(self.data_processor.get_ch_gain_c())
        ch_gain_d = self.data_processor.int_to_float(self.data_processor.get_ch_gain_d())
        self.txt_ch_gain_a.SetValue(str(ch_gain_a))
        self.txt_ch_gain_b.SetValue(str(ch_gain_b))
        self.txt_ch_gain_c.SetValue(str(ch_gain_c))
        self.txt_ch_gain_d.SetValue(str(ch_gain_d))

    def OnUpdate(self, event):
        if self.Validate():
            # Everything is validated, so convert the inputs to floats
            ch_gain_a = float(self.txt_ch_gain_a.GetValue())
            ch_gain_b = float(self.txt_ch_gain_b.GetValue())
            ch_gain_c = float(self.txt_ch_gain_c.GetValue())
            ch_gain_d = float(self.txt_ch_gain_d.GetValue())

            # We then need to convert the values to the IEEE 754 representation as integers
            ch_gain_a = self.data_processor.float_to_int(ch_gain_a)
            ch_gain_b = self.data_processor.float_to_int(ch_gain_b)
            ch_gain_c = self.data_processor.float_to_int(ch_gain_c)
            ch_gain_d = self.data_processor.float_to_int(ch_gain_d)

            # First load the relevant data to the FPGA
            self.data_processor.set_cal_gain_a(ch_gain_a)
            self.data_processor.set_cal_gain_b(ch_gain_b)
            self.data_processor.set_cal_gain_c(ch_gain_c)
            self.data_processor.set_cal_gain_d(ch_gain_d)

            # Then write to the flash buffer
            self.data_processor.wr_flash_buf()
            wx.MessageBox("Ch Gain successfully updated", "Update Successful")


class ChGainValidator(Validator.Validator):
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
            wx.MessageBox("Please enter a value that is within the accepted range (+/- 5.0)", "Out of Range")
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
