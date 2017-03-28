# Panel for editing event parameters (e.g. event length)

import wx


class EventParamPanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

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

    def __set_properties(self):
        pass

    def __do_layout(self):
        # self.event_param_box.Lower()
        sizer_event_param_box = wx.StaticBoxSizer(self.event_param_box, wx.VERTICAL)

        sizer_trig_th = wx.BoxSizer(wx.HORIZONTAL)
        # sizer_trig_th.Add(self.lbl_trig_th, 1, wx.EXPAND, 4)
        sizer_trig_th.Add(self.lbl_trig_th, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_trig_th.Add(self.txt_trig_th, 1, wx.EXPAND)

        sizer_trig_dt = wx.BoxSizer(wx.HORIZONTAL)
        sizer_trig_dt.Add(self.lbl_trig_dt, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_trig_dt.Add(self.txt_trig_dt, 1, wx.EXPAND)

        sizer_trig_dl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_trig_dl.Add(self.lbl_trig_dl, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_trig_dl.Add(self.txt_trig_dl, 1, wx.EXPAND)

        sizer_evt_len = wx.BoxSizer(wx.HORIZONTAL)
        sizer_evt_len.Add(self.lbl_evt_len, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_evt_len.Add(self.txt_evt_len, 1, wx.EXPAND)

        sizer_evt_tail = wx.BoxSizer(wx.HORIZONTAL)
        sizer_evt_tail.Add(self.lbl_evt_tail, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_evt_tail.Add(self.txt_evt_tail, 1, wx.EXPAND)

        sizer_bl_len = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bl_len.Add(self.lbl_bl_len, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_bl_len.Add(self.txt_bl_len, 1, wx.EXPAND)

        sizer_event_param_box.Add(self.btn_update_evt_param, 0, wx.EXPAND, 0)
        sizer_event_param_box.Add(sizer_trig_th, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_trig_dt, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_trig_dl, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_evt_len, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_evt_tail, 0, wx.ALL | wx.EXPAND, 4)
        sizer_event_param_box.Add(sizer_bl_len, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(sizer_event_param_box, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)
