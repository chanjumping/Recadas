import tkinter
from tkinter import *
from tkinter import ttk
from Util.Gui_Su import *
from Util.Gui_SuTer import *
from Util.Gui_SF import *
from Util.Gui_JT808 import *

class MainWindow():
    def __init__(self):
        self.mainwindow = Tk()
        self.mainwindow.title("FuncWindow")
        self.ww = self.mainwindow.winfo_screenwidth()
        self.wh = self.mainwindow.winfo_screenheight()
        self.mw = (self.ww - 800) / 2
        self.mh = (self.wh - 800) / 2
        self.mainwindow.geometry("%dx%d+%d+%d" %(800,800,self.mw,self.mh))
        self.mainwindow.resizable(height=True)
        self.framecontrol = ttk.Notebook(self.mainwindow)
        self.framecontrol.pack(expand=1,fill="both")
        self.bar()
        ttk.Style().configure(".",font=("STxingkai",28),foreground="black")
        self.su = Frame(self.framecontrol)
        self.framecontrol.add(self.su,text="苏标外设")
        self.su_device()
        self.rw = Frame(self.framecontrol)
        self.framecontrol.add(self.rw,text="私有协议")
        self.jt808 = Frame(self.framecontrol)
        self.framecontrol.add(self.jt808,text="JT808协议")
        self.jt_808()
        self.sf = Frame(self.framecontrol)
        self.framecontrol.add(self.sf,text="顺丰协议")
        self.shunfeng()
        self.dev = Frame(self.framecontrol)
        self.framecontrol.add(self.dev,text="苏标终端")
        self.su_terminal()
        self.mainwindow.mainloop()

    def bar(self):
        menuBar = Menu(self.mainwindow)
        self.mainwindow.config(menu=menuBar)
        # Add menu items
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="新建")
        fileMenu.add_separator()
        fileMenu.add_command(label="退出", command="")
        menuBar.add_cascade(label="自分がまだ行けると思うならば、必死にしがみついてみることで自分の限界がまた延び。", menu=fileMenu)

    def grid_conf(self,list):
        for frame in list:
            frame.grid_configure(padx=25,pady=10)
            for child in frame.winfo_children():
                child.grid_configure(padx=1,pady=2)

    #苏标外设
    def su_device(self):
        self.frame_su_common = LabelFrame(self.su, text="通用指令",font=("STxingkai",20))
        self.frame_su_common.grid(row=0, column=0,sticky=W)
        self.frame_su_para = LabelFrame(self.su, text="参数操作",font=("STxingkai",20))
        self.frame_su_para.grid(row=0, column=1,sticky=W)
        self.frame_su_state = LabelFrame(self.su, text="外设状态",font=("STxingkai",20))
        self.frame_su_state.grid(row=1, column=0,sticky=W)
        self.frame_su_picture = LabelFrame(self.su, text="抓拍",font=("STxingkai",20))
        self.frame_su_picture.grid(row=1, column=1,sticky=W)
        self.frame_su_daily = LabelFrame(self.su, text="日志操作",font=("STxingkai",20))
        self.frame_su_daily.grid(row=2, column=0,sticky=W)
        self.frame_su_mode = LabelFrame(self.su, text="模式操作",font=("STxingkai",20))
        self.frame_su_mode.grid(row=2, column=1,sticky=W)
        self.frame_su_upgrade = LabelFrame(self.su, text="升级操作",font=("STxingkai",20))
        self.frame_su_upgrade.grid(row=3, column=0,sticky=W)
        self.frame_su_msg = LabelFrame(self.su, text="构造报文",font=("STxingkai",20))
        self.frame_su_msg.grid(row=3, column=1,sticky=W)
        list = [self.frame_su_common, self.frame_su_para, self.frame_su_state, self.frame_su_picture, self.frame_su_daily,
                     self.frame_su_mode, self.frame_su_upgrade, self.frame_su_msg]
        self.grid_conf(list)
        SuFuncWindow(self.frame_su_common, self.frame_su_para, self.frame_su_state, self.frame_su_picture, self.frame_su_daily,
                     self.frame_su_mode, self.frame_su_upgrade, self.frame_su_msg)

    #苏标终端
    def su_terminal(self):
        self.frame_dev_upgrade = LabelFrame(self.dev,text="升级操作",font=("STxingkai",20))
        self.frame_dev_upgrade.grid(row=0,column=0,sticky=W)
        self.frame_dev_msg = LabelFrame(self.dev,text="构造报文",font=("STxingkai",20))
        self.frame_dev_msg.grid(row=0,column=1,sticky=W)
        self.frame_dev_info = LabelFrame(self.dev,text="基本信息",font=("STxingkai",20))
        self.frame_dev_info.grid(row=1,column=0,sticky=W)
        self.frame_dev_para = LabelFrame(self.dev,text="设置参数",font=("STxingkai",20))
        self.frame_dev_para.grid(row=1,column=1,sticky=W)
        self.frame_dev_tts = LabelFrame(self.dev,text="语音播报",font=("STxingkai",20))
        self.frame_dev_tts.grid(row=2,column=0,sticky=W)
        # self.frame_dev_picture = LabelFrame(self.dev,text="抓拍",font=("STxingkai",20))
        # self.frame_dev_picture.grid(row=2,column=1,sticky=W)
        self.frame_dev_file = LabelFrame(self.dev,text="远程查询",font=("STxingkai",20))
        self.frame_dev_file.grid(row=2,column=1,sticky=W)
        list = [self.frame_dev_upgrade,self.frame_dev_msg,self.frame_dev_info,self.frame_dev_para,
                self.frame_dev_tts,self.frame_dev_file]
        self.grid_conf(list)
        SuTerFuncWindow(self.frame_dev_upgrade, self.frame_dev_msg, self.frame_dev_info, self.frame_dev_para,
                        self.frame_dev_tts, self.frame_dev_file, self.mainwindow)

    #顺丰
    def shunfeng(self):
        self.frame_sf_para = LabelFrame(self.sf,text="参数操作",font=("STxingkai",20))
        self.frame_sf_para.grid(row=0,column=0,sticky=W)
        self.frame_sf_msg = LabelFrame(self.sf,text="构造报文",font=("STxingkai",20))
        self.frame_sf_msg.grid(row=0,column=1,sticky=W)
        self.frame_sf_tts = LabelFrame(self.sf,text="语音播报",font=("STxingkai",20))
        self.frame_sf_tts.grid(row=1,column=0,sticky=W)
        self.frame_sf_upgrade = LabelFrame(self.sf,text="升级操作",font=("STxingkai",20))
        self.frame_sf_upgrade.grid(row=1,column=1,sticky=W)
        list = [self.frame_sf_para,self.frame_sf_msg,self.frame_sf_tts,self.frame_sf_upgrade]
        self.grid_conf(list)
        SFFuncWindow(self.frame_sf_para,self.frame_sf_msg,self.frame_sf_tts,self.frame_sf_upgrade,self.mainwindow)

    #JT808
    def jt_808(self):
        self.frame_jt808_para = LabelFrame(self.jt808,text="参数操作",font=("STxingkai",20))
        self.frame_jt808_para.grid(row=0,column=0,sticky=W)
        self.frame_jt808_msg = LabelFrame(self.jt808,text="构造报文",font=("STxingkai",20))
        self.frame_jt808_msg.grid(row=0,column=1,sticky=W)
        self.frame_jt808_tts = LabelFrame(self.jt808,text="语音播报",font=("STxingkai",20))
        self.frame_jt808_tts.grid(row=1,column=0,sticky=W)
        self.frame_jt808_photo = LabelFrame(self.jt808,text="拍照操作",font=("STxingkai",20))
        self.frame_jt808_photo.grid(row=1,column=1,sticky=W)
        self.frame_jt808_upgrade = LabelFrame(self.jt808,text="升级操作",font=("STxingkai",20))
        self.frame_jt808_upgrade.grid(row=2,column=0,sticky=W)
        self.frame_jt808_reboot = LabelFrame(self.jt808,text="系统重启",font=("STxingkai",20))
        self.frame_jt808_reboot.grid(row=2,column=1,sticky=W)
        list = [self.frame_jt808_para,self.frame_jt808_msg,self.frame_jt808_tts,self.frame_jt808_photo,self.frame_jt808_upgrade,self.frame_jt808_reboot]
        self.grid_conf(list)
        JTFuncWindow(self.frame_jt808_para,self.frame_jt808_msg,self.frame_jt808_tts,self.frame_jt808_photo,self.frame_jt808_upgrade,self.frame_jt808_reboot,self.mainwindow)

if __name__ == "__main__":
    MainWindow()