import wx
import string


class Validator(wx.PyValidator):
    """
    Custom parent validator (Each panel in the GUI inherits from this)
    """

    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        """
        To be implemented by subclasses
        """
        pass

    def Validate(self, parent):
        """
        To be implemented by subclasses
        """
        pass

    def TransferToWindow(self):
        """
        Don't need to worry about this
        """
        return True

    def TransferFromWindow(self):
        """
        Don't need to worry about this
        """
        return True

    def OnChar(self, event):
        """
        Event handler that intercepts invalid key presses, preventing the user from entering letters into a number-only
        field. Subclasses may implement their own version of this method, depending on the input rules.

        Note: The user could theoretically bypass this functionality by pasting letters into a number-only field
        via the clipboard. The Validate() method is responsible for making the final checks on the input.
        """
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
        """
        Checks if val is a string that consists only of digits (0-9)
        :param val: The string to check
        :return: True | False
        """
        for x in val:
            if x not in string.digits:
                return False
        return True

    @staticmethod
    def contains_only_hex(val):
        """
        Checks if val is a string that consists only of hexadecimals (0-9, A-F or a-f)
        :param val: The string to check
        :return: True | False
        """
        for x in val:
            if x not in string.hexdigits:
                return False
        return True

    @staticmethod
    def is_float(val):
        """
        Checks if val is a valid Python float
        :param val: The value to check
        :return: True | False
        """
        try:
            float(val)
        except (ValueError, SyntaxError):
            return False
        return True
