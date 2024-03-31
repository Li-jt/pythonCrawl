import os
import queue
from threading import Thread

import wx
import wx.xrc
from wx.lib.pubsub import pub

from src.index import get_data
import utils.glo as gl


# class MyFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, title='界面')
#         # 创建面板
#         panel = wx.Panel(self)
#         vbox = wx.BoxSizer(wx.VERTICAL)
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL)
#         l1 = wx.StaticText(panel, -1, "文本域")
#         hbox1.Add(l1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
#         self.t1 = wx.TextCtrl(panel)
#         hbox1.Add(self.t1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
#         self.t1.Bind(wx.EVT_TEXT, self.on_key_typed)
#         vbox.Add(hbox1)
#
#     def on_key_typed(self, event):
#         print(event.GetString())


class TestThreading(Thread):
    def __init__(self, search, user, type):
        self.search = search
        self.user = user
        self.type = type
        # 线程实例化时立即启动
        Thread.__init__(self)
        self.start()

    def run(self):
        get_data(self.search, self.user, self.type)


class MyDialog(wx.Dialog):

    def __init__(self, parent, message='请输入数字'):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(273, 105), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, message, wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText8.Wrap(-1)

        bSizer9.Add(self.m_staticText8, 1, wx.ALL, 5)

        bSizer8.Add(bSizer9, 1, wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.m_button2, 0, wx.ALL, 5)

        bSizer8.Add(bSizer10, 1, wx.ALIGN_CENTER, 5)

        self.SetSizer(bSizer8)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_button2.Bind(wx.EVT_BUTTON, self.handler_are_ou_sure)

    def __del__(self):
        self.m_button2.Unbind(wx.EVT_BUTTON, handler=self.handler_are_ou_sure)

    def handler_are_ou_sure(self, event):
        self.Close()


class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=u"界面：关闭界面结束程序", pos=wx.DefaultPosition,
                          size=wx.Size(460, 281),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.type = None
        self.user = None
        self.search = None
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2.SetMinSize(wx.Size(-1, 10))
        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"搜索方式(1:画师id;2:搜索;)：", wx.DefaultPosition,
                                           wx.DefaultSize, wx.ALIGN_RIGHT)
        self.m_staticText2.Wrap(-1)

        self.m_staticText2.SetMinSize(wx.Size(210, -1))

        bSizer2.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_textCtrl3, 1, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer21.SetMinSize(wx.Size(-1, 10))
        self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, u"作品或用户id：", wx.DefaultPosition, wx.DefaultSize,
                                            wx.ALIGN_RIGHT)
        self.m_staticText21.Wrap(-1)

        self.m_staticText21.SetMinSize(wx.Size(210, -1))

        bSizer21.Add(self.m_staticText21, 0, wx.ALL, 5)

        self.m_textCtrl31 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer21.Add(self.m_textCtrl31, 1, wx.ALL, 5)

        bSizer1.Add(bSizer21, 1, wx.EXPAND, 5)

        bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer22.SetMinSize(wx.Size(-1, 10))
        self.m_staticText22 = wx.StaticText(self, wx.ID_ANY, u"类型（1:全部，2:全年龄，3:R-18）：", wx.DefaultPosition,
                                            wx.DefaultSize, wx.ALIGN_RIGHT)
        self.m_staticText22.Wrap(-1)

        self.m_staticText22.SetMinSize(wx.Size(210, -1))

        self.m_staticText22.Disable()

        bSizer22.Add(self.m_staticText22, 0, wx.ALL, 5)

        self.m_textCtrl32 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer22.Add(self.m_textCtrl32, 1, wx.ALL, 5)
        self.m_textCtrl32.Disable()

        bSizer1.Add(bSizer22, 1, wx.EXPAND, 5)

        bSizer221 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer221.SetMinSize(wx.Size(-1, 10))
        self.m_staticText221 = wx.StaticText(self, wx.ID_ANY, u"文件存放路径：", wx.DefaultPosition, wx.DefaultSize,
                                             wx.ALIGN_RIGHT)
        self.m_staticText221.Wrap(-1)

        self.m_staticText221.SetMinSize(wx.Size(85, -1))

        bSizer221.Add(self.m_staticText221, 0, wx.ALL, 5)

        self.m_textCtrl321 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer221.Add(self.m_textCtrl321, 1, wx.ALL, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer221.Add(self.m_button3, 0, wx.ALL, 5)

        bSizer1.Add(bSizer221, 1, wx.EXPAND, 5)
        bSizer2211 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2211.SetMinSize(wx.Size(-1, 10))
        self.m_gauge2 = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.m_gauge2.SetValue(0)
        bSizer2211.Add(self.m_gauge2, 1, wx.ALL, 5)

        self.m_textCtrl12 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_textCtrl12.SetMinSize(wx.Size(80, 17))
        self.m_textCtrl12.SetValue(f'0/0')

        bSizer2211.Add(self.m_textCtrl12, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2211, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer22, 1, wx.EXPAND, 5)

        bSizer1.Add((0, 0), 1, wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        m_sdbSizer1.Realize();

        bSizer1.Add(m_sdbSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.my_dialog = MyDialog(self)
        pub.subscribe(self.update_display, "update")

        # Connect Events
        self.m_textCtrl3.Bind(wx.EVT_TEXT, self.handler_search)
        self.m_textCtrl31.Bind(wx.EVT_TEXT, self.handler_user)
        self.m_textCtrl32.Bind(wx.EVT_TEXT, self.handler_type)
        self.m_textCtrl321.Bind(wx.EVT_TEXT, self.handler_folder)
        self.m_button3.Bind(wx.EVT_BUTTON, self.select_folder)
        self.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.handler_ok)

    def __del__(self):
        # Disconnect Events
        self.m_textCtrl3.Unbind(wx.EVT_TEXT, handler=self.handler_search)
        self.m_textCtrl31.Unbind(wx.EVT_TEXT, handler=self.handler_user)
        self.m_textCtrl32.Unbind(wx.EVT_TEXT, handler=self.handler_type)
        self.m_textCtrl321.Unbind(wx.EVT_TEXT, handler=self.handler_folder)
        self.m_button3.Unbind(wx.EVT_BUTTON, handler=self.select_folder)
        self.m_sdbSizer1OK.Unbind(wx.EVT_BUTTON, handler=self.handler_ok)

    def update_display(self):
        # btn_text
        self.m_sdbSizer1OK.SetLabel(gl.get_value('btn_text', '加载中'))
        total = gl.get_value('total', 0)
        num = gl.get_value('num', 0)
        print(total, num)
        if total == num and gl.get_value('btn_text', '加载中') == '下载完成':
            self.m_sdbSizer1OK.SetLabel('完成')
            self.m_sdbSizer1OK.Enable()
        if total != 0:
            self.m_gauge2.SetValue(int(num / total * 100))
        self.m_textCtrl12.SetValue(f'{num}/{total}')

    # Virtual event handlers, override them in your derived class
    def handler_search(self, event):
        try:
            if event.GetString() != '':
                self.search = int(event.GetString())
                if self.search == 2:
                    self.m_staticText22.Enable()
                    self.m_textCtrl32.Enable()
                else:
                    self.m_staticText22.Disable()
                    self.m_textCtrl32.Disable()
        except:
            if not self.my_dialog.IsShown():
                self.my_dialog.Show()

    def handler_user(self, event):
        if event.GetString() != '':
            self.user = event.GetString()

    def handler_type(self, event):
        try:
            if event.GetString() != '':
                self.type = int(event.GetString())
        except:
            if not self.my_dialog.IsShown():
                self.my_dialog.Show()

    def handler_folder(self, event):
        gl.set_value('path_folder', event.GetString())

    def select_folder(self, event):
        dlg = wx.DirDialog(self, message="选择一个文件", style=wx.FD_OPEN)
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            gl.set_value('path_folder', dlg.GetPath())
            self.m_textCtrl321.SetValue(dlg.GetPath())

        # fp = os.path.join(dlg.GetPath())  # 组装文件地址
        # ###输出到弹出信息窗口的字符拼装。
        # retstr = str(self.get_FileSize(fp)) + "\n" + self.get_FileAccessTime(fp) + "\n" + self.get_FileCreateTime(
        #     fp) + "\n" + self.get_FileModifyTime(fp)
        # self.text_ctrl_2.SetValue(retstr)

        dlg.Destroy()

    def handler_ok(self, event):
        if self.m_sdbSizer1OK.GetLabel() == '完成':
            gl.set_value('total', 0)
            gl.set_value('num', 0)
            self.m_gauge2.SetValue(0)
            self.m_textCtrl12.SetValue(f'0/0')
            self.m_sdbSizer1OK.SetLabel('OK')
        else:
            if not self.search:
                dia = MyDialog(self, '请选择搜索方式')
                if not dia.IsShown():
                    dia.Show()
            elif not self.user:
                dia = MyDialog(self, '请输入作品或用户id')
                if not dia.IsShown():
                    dia.Show()
            elif not gl.get_value('path_folder'):
                dia = MyDialog(self, '请选择文件存放文件夹')
                if not dia.IsShown():
                    dia.Show()
            elif self.search == 2:
                if not self.type:
                    dia = MyDialog(self, '请选择类型')
                    if not dia.IsShown():
                        dia.Show()
                else:
                    TestThreading(self.search, self.user, self.type)
                    self.m_sdbSizer1OK.Disable()
            else:
                TestThreading(self.search, self.user, self.type)
                self.m_sdbSizer1OK.Disable()
