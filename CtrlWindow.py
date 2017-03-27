# Top-level control window

import wx


class CtrlWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title=title)

    def __do_layout(self):
        pass

    def __set_properties(self):
        pass


# For testing purposes; will normally be created via awake.py
if __name__ == '__main__':
    pass
