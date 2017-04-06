import wx
import string
#
# Custom parent validator
#

class Validator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        pass

    # All children have different requirements for validation
    def Validate(self, parent):
        pass

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

    @staticmethod
    def contains_only_digits(val):
        for x in val:
            if x not in string.digits:
                return False
        return True

    @staticmethod
    def contains_only_hex(val):
        for x in val:
            if x not in string.hexdigits:
                return False
        return True

    @staticmethod
    def is_float(val):
        try:
            float(val)
        except (ValueError, SyntaxError):
            return False
        return True
