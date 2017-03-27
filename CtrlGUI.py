import wx

from CtrlWindow import CtrlWindow


class CtrlGUI(wx.App):
    def OnInit(self):
        iconCtrl = wx.Icon('triumf.ico', wx.BITMAP_TYPE_ICO)
        windowCtrl = CtrlWindow(parent=None, title='AWAKE BPM Settings')
        windowCtrl.SetIcon(iconCtrl)
        # windowCtrl.SetMinSize((800, 600))
        self.SetTopWindow(windowCtrl)
        windowCtrl.Show()
        return True


# For testing
if __name__ == '__main__':
    ctrl_window = CtrlGUI(False)
    ctrl_window.MainLoop()
