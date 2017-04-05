# Panel for editing parameters not included in the other panels (e.g. BPM Diameter)

import wx
import string
import Validator


class OtherParamPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_other_param = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_bpm_dia = wx.StaticText(self, wx.ID_ANY, 'BPM:DIA')
        self.txt_bpm_dia = wx.TextCtrl(self, wx.ID_ANY, '')

        self.other_param_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()

    def __set_properties(self):
        # self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.txt_bpm_dia.SetValidator(OtherParamValidator())

    def __do_layout(self):
        sizer_other_param_box = wx.StaticBoxSizer(self.other_param_box, wx.VERTICAL)

        sizer_bpm_dia = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bpm_dia.Add(self.lbl_bpm_dia, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_bpm_dia.Add(self.txt_bpm_dia, 2, wx.EXPAND, 0)

        sizer_other_param_box.Add(self.btn_update_other_param, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_other_param_box.Add(sizer_bpm_dia, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_other_param_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_other_param)

    def OnUpdate(self, event):
        if (self.Validate()):
            bpm_dia = int(self.txt_bpm_dia.GetValue())

            self.data_processor.set_bpm_dia(bpm_dia)
            self.data_processor.wr_flash_buf()

            wx.MessageBox("Other Parameters successfully updated", "Update Successful")


"""
class OtherParamValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return OtherParamValidator()

    def Validate(self, parent):
        textCtrl = self.GetWindow()
        val = textCtrl.GetValue()

        if len(val) == 0:
            wx.MessageBox("BPM DIA value required!", "No Input")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        elif not OtherParamValidator._contains_only_digits(val):
            wx.MessageBox("Please enter numbers only", "Invalid Input")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    @staticmethod
    def _contains_only_digits(val):
        for x in val:
            if x not in string.digits:
                return False
        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        return
"""


class OtherParamValidator(Validator.Validator):
    def __init__(self):
        Validator.Validator.__init__(self)

    def Clone(self):
        return OtherParamValidator()

    def Validate(self, parent):
        textCtrl = self.GetWindow()
        val = textCtrl.GetValue()

        if len(val) == 0:
            wx.MessageBox("BPM DIA value required!", "No Input")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        elif not OtherParamValidator.contains_only_digits(val):
            wx.MessageBox("Please enter numbers only", "Invalid Input")
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
