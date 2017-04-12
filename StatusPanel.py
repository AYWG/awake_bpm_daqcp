# Panel for showing what settings are currently enabled (akin to the LED indicators in the LabVIEW GUI
# (Not required yet)
import wx
from LED import LED

class StatusPanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, name=title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        pass