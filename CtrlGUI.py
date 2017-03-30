import wx

from CtrlWindow import CtrlWindow


class CtrlGUI(wx.App):
    # We need a custom constructor so that we can get access to the data_processor object
    def __init__(self, data_processor):
        self.data_processor = data_processor
        wx.App.__init__(self, False)

    def OnInit(self):
        iconCtrl = wx.Icon('triumf.ico', wx.BITMAP_TYPE_ICO)
        windowCtrl = CtrlWindow(parent=None, title='AWAKE BPM Settings', data_processor=self.data_processor)
        windowCtrl.SetIcon(iconCtrl)
        self.SetTopWindow(windowCtrl)
        windowCtrl.Show()
        return True


# For testing
# if __name__ == '__main__':
#     ctrl_window = CtrlGUI(False)
#     ctrl_window.MainLoop()
