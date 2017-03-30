# Top-level control window

import wx
import AddressPanel
import AFECtrlPanel
import CalGainPanel
import ChGainPanel
import EventParamPanel
import FlashReadWritePanel
import ModePanel
import OtherParamPanel
import StatusPanel


class CtrlWindow(wx.Frame):
    def __init__(self, parent, title, data_processor):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title=title)

        # Add panels
        self.address_panel = AddressPanel.AddressPanel(parent=self, title='Addresses', data_processor=data_processor)
        self.afectrl_panel = AFECtrlPanel.AFECtrlPanel(parent=self, title='AFE Control Register',
                                                       data_processor=data_processor)
        self.calgain_panel = CalGainPanel.CalGainPanel(parent=self, title='Cal Gain Adj.',
                                                       data_processor=data_processor)
        self.chgain_panel = ChGainPanel.ChGainPanel(parent=self, title='Channel Gain Adj.',
                                                    data_processor=data_processor)
        self.eventparam_panel = EventParamPanel.EventParamPanel(parent=self, title='Event Parameters',
                                                                data_processor=data_processor)
        self.flashrdwr_panel = FlashReadWritePanel.FlashReadWritePanel(parent=self, title='Flash Read/Write',
                                                                       data_processor=data_processor)
        self.mode_panel = ModePanel.ModePanel(parent=self, title='Mode Register', data_processor=data_processor)
        self.otherparam_panel = OtherParamPanel.OtherParamPanel(parent=self, title='Other Parameters',
                                                                data_processor=data_processor)
        # self.status_panel = StatusPanel.StatusPanel(parent=self, title='Status')

        # Add event bindings

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        # Light-grey
        self.SetBackgroundColour(wx.Colour(240, 240, 240))

    def __do_layout(self):
        sizer_btm_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btm_row.Add(self.eventparam_panel, 1, wx.EXPAND | wx.ALL, 0)
        sizer_btm_row.Add(self.chgain_panel, 1, wx.EXPAND | wx.ALL, 0)
        sizer_btm_row.Add(self.calgain_panel, 1, wx.EXPAND | wx.ALL, 0)
        sizer_btm_row.Add(self.otherparam_panel, 1, wx.EXPAND | wx.ALL, 0)

        sizer_mid_right = wx.BoxSizer(wx.VERTICAL)
        sizer_mid_right.Add(self.flashrdwr_panel, 0, wx.EXPAND | wx.ALL, 4)
        sizer_mid_right.Add(self.afectrl_panel, 1, wx.EXPAND | wx.ALL, 4)
        sizer_mid_right.Add(self.address_panel, 0, wx.EXPAND | wx.ALL, 4)

        sizer_mid_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mid_row.Add(self.mode_panel, 1, wx.EXPAND | wx.ALL, 4)
        sizer_mid_row.Add(sizer_mid_right, 1, wx.EXPAND | wx.ALL, 4)

        # sizer_top_row = wx.BoxSizer(wx.HORIZONTAL)
        # sizer_top_row.Add(self.status_panel, 1, wx.EXPAND | wx.ALL, 4)

        sizer_vert = wx.BoxSizer(wx.VERTICAL)
        # sizer_vert.Add(sizer_top_row, 1, wx.EXPAND)
        sizer_vert.Add(sizer_mid_row, 2, wx.EXPAND)
        sizer_vert.Add(sizer_btm_row, 1, wx.EXPAND)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_vert, 1, wx.EXPAND)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

        # Set the minimum size of the window once all of the sizers have been set up.
        self.SetMinSize(self.GetSize())
