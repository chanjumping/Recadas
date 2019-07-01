import tkinter
from tkinter import *
from Util.Gui_Su import SuFuncWindow
# from Util.Gui_Jt808 import *


class MainWindow():
    def __init__(self):
        self.mainwindow = Tk()
        self.mainwindow.title("主功能窗口")
        self.ww = self.mainwindow.winfo_screenwidth()
        self.wh = self.mainwindow.winfo_screenheight()
        self.mw = (self.ww - 700) / 2
        self.mh = (self.wh - 600) / 2
        self.mainwindow.geometry("%dx%d+%d+%d" %(800, 600, self.mw, self.mh))
        self.mainwindow.resizable(height=True)
        self.frame_main = Frame(self.mainwindow)
        self.frame_main.pack()
        self.button_su = Button(self.frame_main, text="苏标协议", command=self.su_FuncModule, bd=15, width=40)
        self.button_su.pack(pady=20, ipady=10)
        self.button_rw = Button(self.frame_main, text="瑞为协议", command=self.rw_FuncModule, bd=15, width=40)
        self.button_rw.pack(pady=20, ipady=10)
        self.button_808 = Button(self.frame_main, text="JT808协议", command=self.jt_FuncModule, bd=15, width=40)
        self.button_808.pack(pady=20, ipady=10)
        self.button_sf = Button(self.frame_main, text="顺丰协议", command=self.sf_FuncModule, bd=15, width=40)
        self.button_sf.pack(pady=20, ipady=10)
        self.button_su_dev = Button(self.frame_main, text="苏标终端协议", command=self.dev_FuncModule, bd=15, width=40)
        self.button_su_dev.pack(pady=20, ipady=10)
        self.mainwindow.mainloop()

    # 苏标
    def su_FuncModule(self):
        self.frame_main.destroy()
        SuFuncWindow(self.mainwindow)

    # 私有
    def rw_FuncModule(self):
        self.frame_main.destroy()

    # JT808
    def jt_FuncModule(self):
        self.frame_main.destroy()
        JtFuncWindow(self.mainwindow)

    # 顺丰
    def sf_FuncModule(self):
        self.frame_main.destroy()

    # 苏标终端
    def dev_FuncModule(self):
        self.frame_main.destroy()


if __name__ == "__main__":
    MainWindow()     