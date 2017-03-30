# Panel for editing event parameters (e.g. event length)

import wx


class EventParamPanel(wx.Panel):
    def __init__(self, parent, title, data_processor):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_processor = data_processor
        self.btn_update_evt_param = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_trig_th = wx.StaticText(self, wx.ID_ANY, 'TRIG:TH')
        self.txt_trig_th = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_trig_dt = wx.StaticText(self, wx.ID_ANY, 'TRIG:DT')
        self.txt_trig_dt = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_trig_dl = wx.StaticText(self, wx.ID_ANY, 'TRIG:DL')
        self.txt_trig_dl = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_evt_len = wx.StaticText(self, wx.ID_ANY, 'EVT:LEN')
        self.txt_evt_len = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_evt_tail = wx.StaticText(self, wx.ID_ANY, 'EVT:TAIL')
        self.txt_evt_tail = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lbl_bl_len = wx.StaticText(self, wx.ID_ANY, 'BL:LEN')
        self.txt_bl_len = wx.TextCtrl(self, wx.ID_ANY, '')

        self.event_param_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()
        self.__attach_events()

    def __set_properties(self):
        pass

    def __do_layout(self):

        sizer_event_param_box = wx.StaticBoxSizer(self.event_param_box, wx.VERTICAL)

        sizer_trig_th = wx.BoxSizer(wx.HORIZONTAL)
        sizer_trig_th.Add(self.lbl_trig_th, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_trig_th.Add(self.txt_trig_th, 2, wx.EXPAND)

        sizer_trig_dt = wx.BoxSizer(wx.HORIZONTAL)
        sizer_trig_dt.Add(self.lbl_trig_dt, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_trig_dt.Add(self.txt_trig_dt, 2, wx.EXPAND)

        sizer_trig_dl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_trig_dl.Add(self.lbl_trig_dl, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_trig_dl.Add(self.txt_trig_dl, 2, wx.EXPAND)

        sizer_evt_len = wx.BoxSizer(wx.HORIZONTAL)
        sizer_evt_len.Add(self.lbl_evt_len, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_evt_len.Add(self.txt_evt_len, 2, wx.EXPAND)

        sizer_evt_tail = wx.BoxSizer(wx.HORIZONTAL)
        sizer_evt_tail.Add(self.lbl_evt_tail, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_evt_tail.Add(self.txt_evt_tail, 2, wx.EXPAND)

        sizer_bl_len = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bl_len.Add(self.lbl_bl_len, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_bl_len.Add(self.txt_bl_len, 2, wx.EXPAND)

        sizer_event_param_box.Add(self.btn_update_evt_param, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_event_param_box.Add(sizer_trig_th, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_trig_dt, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_trig_dl, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_evt_len, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_evt_tail, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_bl_len, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_event_param_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)

    def __attach_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnUpdate, self.btn_update_evt_param)

    def OnUpdate(self):
        # Do validation here?

        # Everything is validated, so convert the inputs to floats
        trig_th = float(self.txt_trig_th.GetValue())
        trig_dt = float(self.txt_trig_dt.GetValue())
        trig_dl = float(self.txt_trig_dl.GetValue())
        evt_len = float(self.txt_evt_len.GetValue())
        evt_tail = float(self.txt_evt_tail.GetValue())
        bl_len = float(self.txt_bl_len.GetValue())

        # First load the relevant data to the FPGA
        self.data_processor.set_trig_th(trig_th)
        self.data_processor.set_trig_dt(trig_dt)
        self.data_processor.set_trig_dl(trig_dl)
        self.data_processor.set_evt_len(evt_len)
        self.data_processor.set_evt_tail(evt_tail)
        self.data_processor.set_bl_len(bl_len)

        # Then write to the flash buffer
        self.data_processor.wr_flash_buf()