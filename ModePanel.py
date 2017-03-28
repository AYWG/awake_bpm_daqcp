# Panel for setting the BPM mode

import wx


class ModePanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, name=title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        pass



