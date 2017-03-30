# Panel for editing parameters not included in the other panels (e.g. BPM Diameter)

import wx


class OtherParamPanel(wx.Panel):
    def __init__(self, parent, title):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.btn_update_other_param = wx.Button(self, wx.ID_ANY, 'Update')
        self.lbl_bpm_dia = wx.StaticText(self, wx.ID_ANY, 'BPM:DIA')
        self.txt_bpm_dia = wx.TextCtrl(self, wx.ID_ANY, '')

        self.other_param_box = wx.StaticBox(self, wx.ID_ANY, title)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_other_param_box = wx.StaticBoxSizer(self.other_param_box, wx.VERTICAL)

        sizer_bpm_dia = wx.BoxSizer(wx.HORIZONTAL)
        sizer_bpm_dia.Add(self.lbl_bpm_dia, 1, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer_bpm_dia.Add(self.txt_bpm_dia, 2, wx.EXPAND, 0)

        sizer_other_param_box.Add(self.btn_update_other_param, 0, wx.SHAPED | wx.ALIGN_CENTER, 0)
        sizer_other_param_box.Add(sizer_bpm_dia, 0, wx.ALL | wx.EXPAND, 4)

        sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_main.Add(sizer_other_param_box, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_main)
        self.SetAutoLayout(True)
        sizer_main.Fit(self)
