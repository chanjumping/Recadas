from tkinter import *
from tkinter import Radiobutton
from Util.GlobalVar import *
from Util.CommonMethod import *
import Util.GlobalVar as GlobalVar
from tkinter import messagebox

class DevFuncWindow():
    def __init__(self,upgrade,msg,info,para,tts,file,mainwindow):
        self.frame_dev_upgrade = upgrade
        self.frame_dev_msg = msg
        self.frame_dev_info = info
        self.frame_dev_para = para
        self.frame_dev_tts = tts
        # self.frame_dev_photo = photo
        self.frame_dev_file = file
        self.mainwindow = mainwindow
        self.serial_num = "0000"
        self.agreement_sign = "7E"
        self.dev_FuncWindow()

    def dev_FuncWindow(self):
        self.frame_upgrade_path = StringVar()
        self.frame_msg = StringVar()
        self.frame_trans = StringVar()
        self.frame_devid = StringVar()
        self.frame_ip = StringVar()
        self.frame_port = StringVar()
        self.frame_tts = StringVar()
        self.frame_pass = StringVar()
        self.frame_size = StringVar()
        self.frame_name = StringVar()
        self.frame_flag = StringVar()
        #升级操作
        self.frame_dev_upgrade_direct = Label(self.frame_dev_upgrade,text="升级包地址：")
        self.frame_dev_upgrade_direct.grid(row=0,column=0,ipadx=20,ipady=5,padx=5,pady=5,sticky=W)
        self.frame_dev_upgrade_path = Entry(self.frame_dev_upgrade,textvariable=self.frame_upgrade_path,bd=5,width=18)
        self.frame_dev_upgrade_path.grid(row=0,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        self.frame_dev_upgrade_example = Label(self.frame_dev_upgrade,text="例如：ftp://test:123@1.1.1.1/Package.zip;;",fg="red")
        self.frame_dev_upgrade_example.grid(row=1,column=0,columnspan=2,ipadx=20,sticky=E)
        self.frame_dev_upgrade_exe = Button(self.frame_dev_upgrade,text="开始升级",command=self.start_upgrade,bd=5)
        self.frame_dev_upgrade_exe.grid(row=2,column=1,ipadx=20,ipady=5,pady=5,padx=20,sticky=W)
        #构造报文
        self.frame_dev_msg_text = Label(self.frame_dev_msg, text="构造的报文：")
        self.frame_dev_msg_text.grid(row=0, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_msg_cont = Entry(self.frame_dev_msg, textvariable=self.frame_msg,bd=5,width=17)
        self.frame_dev_msg_cont.grid(row=0, column=1, ipadx=20, ipady=5, pady=5,padx=20, sticky=W)
        self.frame_dev_msg_example = Label(self.frame_dev_msg,text="例如：7E 89 00 **** 4D 7E",fg="red")
        self.frame_dev_msg_example.grid(row=1,column=1,ipadx=20,padx=5,sticky=W)
        self.frame_dev_msg_exe = Button(self.frame_dev_msg, text="发   送", command=self.send_msg, bd=5)
        self.frame_dev_msg_exe.grid(row=2, column=1, ipadx=20, ipady=5, pady=5,padx=20, sticky=W)
        #基本信息查询
        self.frame_dev_info_trans = Label(self.frame_dev_info,text="透传类型：",width=10)
        self.frame_dev_info_trans.grid(row=0, column=0, ipadx=10, ipady=5, pady=5, sticky=W)
        self.frame_dev_info_f7 = Radiobutton(self.frame_dev_info,text="状态",variable=self.frame_trans,value="F7",indicatoron=0,bd=4)
        self.frame_dev_info_f7.grid(row=0,column=1,columnspan=2,padx=20,pady=2,ipady=5,sticky=W)
        self.frame_dev_info_f8 = Radiobutton(self.frame_dev_info,text="信息",variable=self.frame_trans,value="F8",indicatoron=0,bd=4)
        self.frame_dev_info_f8.grid(row=0,column=3,columnspan=2,padx=20,pady=2,ipady=5,sticky=W)
        self.frame_dev_info_id = Label(self.frame_dev_info,text="外设ID：",width=10)
        self.frame_dev_info_id.grid(row=1, column=0, ipadx=5, ipady=5, pady=5, sticky=W)
        self.frame_dev_info_64 = Radiobutton(self.frame_dev_info,text="ADAS",variable=self.frame_devid,value="64",bd=4)
        self.frame_dev_info_64.grid(row=1,column=1,pady=5,ipady=5, sticky=W)
        self.frame_dev_info_65 = Radiobutton(self.frame_dev_info,text="DSM",variable=self.frame_devid,value="65",bd=4)
        self.frame_dev_info_65.grid(row=1,column=2,pady=5,ipady=5,sticky=W)
        self.frame_dev_info_66 = Radiobutton(self.frame_dev_info,text="TPMS",variable=self.frame_devid,value="66",bd=4)
        self.frame_dev_info_66.grid(row=1,column=3,pady=5,ipady=5,sticky=W)
        self.frame_dev_info_67 = Radiobutton(self.frame_dev_info,text="BSD",variable=self.frame_devid,value="67",bd=4)
        self.frame_dev_info_67.grid(row=1,column=4,pady=5,ipady=5,sticky=W)
        self.frame_dev_info_query = Button(self.frame_dev_info,text="查    询",command=self.query_info,bd=5)
        self.frame_dev_info_query.grid(row=2, column=1,columnspan=4, ipadx=20, ipady=5, pady=5,padx=50, sticky=W)
        #设置参数
        self.frame_dev_para_ip = Label(self.frame_dev_para,text="IP地址：",width=10)
        self.frame_dev_para_ip.grid(row=0, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_para_ipcont = Entry(self.frame_dev_para,textvariable=self.frame_ip,bd=5,width=17)
        self.frame_dev_para_ipcont.grid(row=0, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_para_port = Label(self.frame_dev_para,text="端口号：",width=10)
        self.frame_dev_para_port.grid(row=1, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_para_portcont = Entry(self.frame_dev_para,textvariable=self.frame_port,bd=5,width=17)
        self.frame_dev_para_portcont.grid(row=1, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_para_query = Button(self.frame_dev_para,text="查   询",command=self.query_para,bd=5)
        self.frame_dev_para_query.grid(row=2, column=0, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_para_exe = Button(self.frame_dev_para,text="设   置",command=self.send_msg,bd=5)
        self.frame_dev_para_exe.grid(row=2, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        #tts语音
        self.frame_dev_tts_flag = Label(self.frame_dev_tts,text="TTS标记：",width=10)
        self.frame_dev_tts_flag.grid(row=0, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_tts_flagcont = Entry(self.frame_dev_tts,textvariable=self.frame_flag,width=18,bd=5)
        self.frame_dev_tts_flagcont.grid(row=0, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_tts_voice = Label(self.frame_dev_tts,text="语音内容：",width=10)
        self.frame_dev_tts_voice.grid(row=1, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        self.frame_dev_tts_voicecont = Entry(self.frame_dev_tts,textvariable=self.frame_tts,width=18,bd=5)
        self.frame_dev_tts_voicecont.grid(row=1, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        self.frame_dev_tts_exe = Button(self.frame_dev_tts,text="播    报",command=self.broadcast_vioce,bd=5)
        self.frame_dev_tts_exe.grid(row=2, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        #立即拍照
        # self.frame_dev_photo_title = Label(self.frame_dev_photo,text="通道ID：",width=10)
        # self.frame_dev_photo_title.grid(row=0, column=0, ipadx=20, ipady=5,padx=5, pady=5, sticky=W)
        # self.frame_dev_photo_type = Entry(self.frame_dev_photo,textvariable=self.frame_pass,width=17,bd=5)
        # self.frame_dev_photo_type.grid(row=0, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        # self.frame_dev_photo_exe = Button(self.frame_dev_photo,text="立即抓拍",command=self.take_photo,bd=5)
        # self.frame_dev_photo_exe.grid(row=1, column=1, ipadx=20, ipady=5,padx=20, pady=5, sticky=W)
        #远程查询告警附件
        self.frame_dev_remote = Button(self.frame_dev_file,text="【点击】远程查询",command=self.window_remote,width=18,bd=5)
        self.frame_dev_remote.grid(row=0,column=0,ipadx=10, ipady=5,padx=90, pady=30, sticky=W)


    # ftp://test:123456@121.40.90.148/RW_CA_V410R004B001-1-002_inc.zip;;
    def start_upgrade(self):
        self.upgrade_path = self.frame_upgrade_path.get()
        msg_body = '01' + byte2str(self.upgrade_path.encode("gbk"))
        body = '8105' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(
            GlobalVar.get_serial_no()) + msg_body
        data = JT808_FLAG + body + calc_check_code(body) + JT808_FLAG
        send_queue.put(data)

    #构造报文
    def send_msg(self):
        self.msg = self.frame_msg.get()
        send_queue.put(self.msg)

    #查询信息
    def query_info(self):
        self.trans = self.frame_trans.get()
        self.id = self.frame_devid.get()
        msg_body = self.trans + "01" + self.id
        body = "8900" + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + self.serial_num + msg_body
        data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
        send_queue.put(data)

    #查询参数
    def query_para(self):
        pass

    #设置参数
    def set_para(self):
        self.ip = self.frame_ip.get()
        self.port = self.frame_port.get()
        number = 0
        msg_body = ""
        if self.ip:
            number+=1
            msg_body += "00000013" + num2big(len(self.ip),1) + str2hex(self.ip,len(self.ip))
        if self.port:
            number+=1
            msg_body += "00000018" + "04" + num2big(int(self.port),4)
        if number:
            msg_body = num2big(number,1) + msg_body
            body = "8103" + num2big(int(len(msg_body)/2),2) + GlobalVar.DEVICEID + self.serial_num + msg_body
            data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
            send_queue.put(data)

    #TTS语音
    def broadcast_vioce(self):
        self.flag = self.frame_flag.get()
        self.tts = self.frame_tts.get()
        if self.tts:
            if self.flag:
                tts_flag = num2big(int(self.flag), 1)
            else:
                tts_flag = '08'
            msg_body = tts_flag + byte2str(self.tts.encode('gbk'))
            body = '8300' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + \
                   self.serial_num + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    #立即拍照
    def take_photo(self):
        pass

    #远程查看告警附件
    def query_file(self):
        self.ip = self.frame_ip.get()
        self.port = self.frame_port.get()
        self.flag = self.frame_flag.get()
        self.name = self.frame_name.get()
        if self.ip and self.port and self.flag:
            msg_body = num2big(len(self.ip),1) + str2hex(self.ip,len(self.ip)) + num2big(int(self.port),4)\
                       + "0000" + self.flag + num2big(len(self.name),1) + str2hex(self.name,len(self.name))
            body = "9211" + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + self.serial_num + msg_body
            data = self.agreement_sign + body + calc_check_code(body) + self.agreement_sign
            send_queue.put(data)
        else:
            messagebox.showerror(title="error",message="Parameter Error")
        self.window_remotequery.destroy()

    def window_remote(self):
        self.window_remotequery = Toplevel(self.mainwindow)
        self.ww = self.window_remotequery.winfo_screenwidth()
        self.wh = self.window_remotequery.winfo_screenheight()
        self.mw = (self.ww - 400)/2
        self.mh = (self.wh - 300)/2
        self.window_remotequery.geometry("%dx%d+%d+%d" %(400,300,self.mw,self.mh))
        self.window_remotequery.title("远程查询告警附件")

        self.frame_dev_file_ip = Label(self.window_remotequery, text="服务器地址：", width=10)
        self.frame_dev_file_ip.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_ipcont = Entry(self.window_remotequery, textvariable=self.frame_ip, width=18, bd=5)
        self.frame_dev_file_ipcont.grid(row=0, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_port = Label(self.window_remotequery, text="服务器端口：", width=10)
        self.frame_dev_file_port.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_portcont = Entry(self.window_remotequery, textvariable=self.frame_port, width=18, bd=5)
        self.frame_dev_file_portcont.grid(row=1, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_flag = Label(self.window_remotequery, text="报警标识号：", width=10)
        self.frame_dev_file_flag.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_flagcont = Entry(self.window_remotequery, textvariable=self.frame_flag, width=18, bd=5)
        self.frame_dev_file_flagcont.grid(row=2, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_name = Label(self.window_remotequery, text="文件名称：", width=10)
        self.frame_dev_file_name.grid(row=3, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        self.frame_dev_file_namecont = Entry(self.window_remotequery, textvariable=self.frame_name, width=18, bd=5)
        self.frame_dev_file_namecont.grid(row=3, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)
        self.frame_dev_file_exe = Button(self.window_remotequery, text="查    询", command=self.query_file, bd=5)
        self.frame_dev_file_exe.grid(row=4, column=1, ipadx=20, ipady=5, padx=20, pady=5, sticky=W)




