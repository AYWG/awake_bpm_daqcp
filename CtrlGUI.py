import wx

# from CtrlWindow import CtrlWindow
from CtrlFrame import CtrlFrame


class CtrlGUI(wx.App):
    # We need a custom constructor so that we can get access to the data_processor object
    def __init__(self, data_processor):
        self.data_processor = data_processor
        wx.App.__init__(self, False)

    def OnInit(self):
        iconCtrl = wx.Icon('triumf.ico', wx.BITMAP_TYPE_ICO)
        frameCtrl = CtrlFrame(parent=None, title='AWAKE BPM Settings', data_processor=self.data_processor)
        frameCtrl.SetIcon(iconCtrl)
        self.SetTopWindow(frameCtrl)
        frameCtrl.Show()
        frameCtrl.Maximize(True)
        return True
