import wx

from src.view.index import MyFrame, MyLogin
import utils.glo as gl

if __name__ == '__main__':
    gl._init()
    app = wx.App()
    # 创建窗口
    frame = MyFrame()
    # frame = MyLogin()
    frame.Centre()
    frame.Show()

    # 进入主循环，让窗口一直显示
    app.MainLoop()
