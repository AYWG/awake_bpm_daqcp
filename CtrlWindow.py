import wx
import wx.lib.scrolledpanel as scrolled
from Panels import (
    AFECtrlPanel,
    AddressPanel,
    CalGainPanel,
    ChGainPanel,
    EventNumPanel,
    EventParamPanel,
    FIFOOccupancyPanel,
    FlashReadWritePanel,
    ModePanel,
    OtherParamPanel,
    StatusPanel
)


class CtrlWindow(scrolled.ScrolledPanel):
    """
    Main window of the GUI that houses all of the different panels needed for AWAKE BPM.
    Implemented for the sake of having a top-level class that inherits scrolling functionality
    (wx.Frame does not)
    """

    def __init__(self, parent, data_processor):
        scrolled.ScrolledPanel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.data_processor = data_processor

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
        self.status_panel = StatusPanel.StatusPanel(parent=self, title='Status', data_processor=data_processor)
        self.fifo_occupancy_panel = FIFOOccupancyPanel.FIFOOccupancyPanel(parent=self, title='FIFO Occupancy', data_processor=data_processor)
        self.event_num_panel = EventNumPanel.EventNumPanel(parent=self, title='Event #', data_processor=data_processor)

        self.__set_properties()
        self.__do_layout()

        self.__attach_events()
        # Enables scrolling when not all the contents of this window are visible in the top-level frame
        self.SetupScrolling()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_btm_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btm_row.Add(self.eventparam_panel, 1, wx.EXPAND | wx.ALL, 0)
        sizer_btm_row.Add(self.chgain_panel, 1, wx.EXPAND | wx.ALL, 0)
        sizer_btm_row.Add(self.calgain_panel, 1, wx.EXPAND | wx.ALL, 0)
        sizer_btm_row.Add(self.otherparam_panel, 1, wx.EXPAND | wx.ALL, 0)

        sizer_mid_right_top = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mid_right_top.Add(self.flashrdwr_panel, 0, wx.EXPAND, 0)
        sizer_mid_right_top.Add(self.fifo_occupancy_panel, 0, wx.EXPAND, 0)
        sizer_mid_right_top.Add(self.event_num_panel, 0, wx.EXPAND, 0)

        sizer_mid_right = wx.BoxSizer(wx.VERTICAL)
        sizer_mid_right.Add(sizer_mid_right_top, 0, wx.EXPAND | wx.ALL, 4)
        sizer_mid_right.Add(self.afectrl_panel, 0, wx.EXPAND | wx.ALL, 4)
        sizer_mid_right.Add(self.address_panel, 0, wx.EXPAND | wx.ALL, 4)

        sizer_mid_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer_mid_row.Add(self.mode_panel, 0, wx.EXPAND | wx.ALL, 4)
        sizer_mid_row.Add(sizer_mid_right, 0, wx.EXPAND | wx.ALL, 4)

        sizer_top_row = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top_row.Add(self.status_panel, 1, wx.SHAPED | wx.ALL, 4)

        sizer_vert = wx.BoxSizer(wx.VERTICAL)
        sizer_vert.Add(sizer_top_row, 0, wx.EXPAND)
        sizer_vert.Add(sizer_mid_row, 0, wx.EXPAND)
        sizer_vert.Add(sizer_btm_row, 0, wx.EXPAND)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_vert, 0, wx.SHAPED)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.update_controls)

    def update_controls(self, event):
        """
        Update all the panels
        """
        self.address_panel.initialize_controls()
        self.afectrl_panel.initialize_controls()
        self.calgain_panel.initialize_controls()
        self.chgain_panel.initialize_controls()
        self.eventparam_panel.initialize_controls()
        self.mode_panel.initialize_controls()
        self.otherparam_panel.initialize_controls()
        self.status_panel.initialize_controls()
        # No data in the flash for fifo occupancy and event num, so those panels are ignored

        # This event handler is only executed as the last step for a flash read
        wx.MessageBox("Flash Read Successful - All Settings Updated", "Success")
