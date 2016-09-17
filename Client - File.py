import threading
from tkinter import *
import socket
import time
import re
from os import system

version = "0.01.001"

name=''
users=[]

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.name_root = Tk()
        self.name_root.title("채팅")

        self.name_frame = Frame(self.name_root)
        self.name_frame.pack()

        Label(self.name_frame, text="닉네임").pack(side=LEFT)
        self.name_entry = Entry(self.name_frame)
        self.name_entry.pack(fill=X, side=LEFT)
        Button(self.name_frame, text="확인", command=self.__name_init__).pack(side=LEFT)
        self.warning_label = Label(self.name_frame, text="(최소 2글자, 최대 20글자)")
        self.warning_label.pack(side=LEFT)

        self.name_root.bind("<Return>", self.__name_init__)

        self.name_root.mainloop()

    def __name_init__(self, event=None):
        global name
        name = self.name_entry.get()
        if 2<=len(name)<=20:
            self.name_root.destroy()
            del(self.name_root, self.name_frame, self.name_entry, self.warning_label)
            self.start()
            Reciever.start()
            
        else:
            self.warning_label.config(fg='red')
        
    def run(self):
        root = Tk()
        root.title("채팅")
        root.geometry("650x630")
        root.minsize(655,632)
        #root.maxsize(650,630)
        
        self.frame = Frame(root)
        self.frame.pack()
        
        self.frame1 = Frame(self.frame)
        self.frame1.pack(side='bottom',fill='x')
                
        self.frame2 = Frame(self.frame1)
        self.frame2.pack(side='right')

        self.frame3 = Frame(self.frame1)
        self.frame3.pack()

        #채팅창
        self.chat_text = Text(self.frame, width=60, padx=2, pady=2, height=40, state=DISABLED)
        self.chat_text_scroll = Scrollbar(self.frame,command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=self.chat_text_scroll.set)
        self.chat_text.pack(side='left',fill='y')
        self.chat_text_scroll.pack(side='left',fill='y')

        #유저 리스트
        self.user_list = Listbox(self.frame)
        self.user_scroll = Scrollbar(self.frame,command=self.user_list.yview)
        self.user_list.configure(width=27, yscrollcommand=self.user_scroll.set)
        self.user_list.pack(side='left',fill='y')
        self.user_scroll.pack(side='left',fill='y')

        #전송 버튼
        send_image = PhotoImage(file='C:\\Users\\ysj\\Desktop\\python\\Networking\\gavel.gif')
        self.send_button = Button(self.frame2,image=send_image, command=self.send_Msg)
        self.send_button.pack()
        self.send_button.bind("<Return>",self.send_Msg)

        #닉네임과 볼륨
        Label(self.frame3, text="닉네임 : "+name).pack(side='left',anchor='w',padx=30,fill='x')
        Label(self.frame3, text='0').pack(side='left')
        self.volume = 100
        self.volume_scale = Scale(self.frame3,orient='horizontal',showvalue=0)
        self.volume_scale.set(100)
        self.volume_scale.configure(command=self.set_Volume)
        self.volume_scale.pack(side='left',anchor='e')
        Label(self.frame3, text='100').pack(side='left',anchor='e')
        self.volume_scale.bind('<ButtonRelease-1>',self.set_Volume)
        
        #입력창
        self.input_text = Text(self.frame1,height=6,padx=2,pady=2)
        self.input_text.pack(side=BOTTOM,fill=BOTH)
        
        self.input_text.bind("<Return>",self.send_Msg)
        self.input_text.bind("<Shift-Return>",self.change_line)

        root.mainloop()
        
    def add_User(self, name, mode=None):
        global users
        users.append(name)
        
        self.user_list.insert(END, name)
        if mode == "Login":
            self.get_Msg(name+" 님이 접속하셨습니다.")
        
    def remove_User(self, name):
        global users
        for u in users:
            if u == name:
                users.remove(u)
                break
        
        for i in range(self.user_list.size()):
            if self.user_list.get(i) == name:
                self.user_list.delete(i)
                break

        self.get_Msg(name+" 님이 퇴장하셨습니다.")
    
    def send_Msg(self, event=None):
        MSG = self.input_text.get(1.0, END).rstrip()
        if MSG:
            Reciever.socket.send(bytes("<Msg>"+MSG+"<End_Msg>\n",'utf-8'))
        self.input_text.delete(1.0, END)

    def change_line(self, event): return

    def get_Msg(self, msg):
        self.chat_text.configure(state=NORMAL)
        flag = False
        if self.chat_text_scroll.get()[1]>=0.99:
            flag = True
        self.chat_text.insert(END, msg+'\n')
        if flag:
            self.chat_text.yview_moveto(1)
            flag = False
        self.chat_text.configure(state=DISABLED)
        
    def set_Volume(self,event):
        self.volume = self.volume_scale.get()     
        

class Network(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.socket = socket.socket()
        host = 'Gibbs.server.ne.kr'
        port = 25565
        self.socket.connect((host, port))
        self.socket.send(bytes("<Version>"+version+"<End_Version>\n",'utf-8'))
        recent_version = re.search("\<(\w+)\>(.*)\<(End\w*)\>\n", self.socket.recv(64).decode()).group(2)
        print(recent_version)
        if version < recent_version:
            os.system("Update.exe")
            exit()

    def run(self):
        self.socket.send(bytes("<Login>"+name+"<End_Login>\n",'utf-8'))
        while True:
            recv = self.socket.recv(1024)
            recv_de = recv.decode()
            print(repr(recv_de))
            recv_re = re.search("\<(\w+)\>(.*)\<(End\w*)\>\n", recv_de, re.DOTALL)
            mode1 = recv_re.group(1)
            instance = recv_re.group(2)
            mode2 = recv_re.group(3)
            print("recv_re:", mode1, instance, mode2)

            if mode1 == "Name":
                Interface.add_User(instance, mode1)
            elif mode1 == "Login":
                Interface.add_User(instance, mode1)
            elif mode1 == "Msg":
                Interface.get_Msg(instance)
            elif mode1 == "Logout":
                Interface.remove_User(instance)

##                elif w.startswith("<File>"):
##                    Fsize = int(Words[1][6:])
##                    FSdisp="Bytes"
##    ##                FSflag = 1
##    ##                while Fsize > 1024:
##    ##                    Fsize = Fsize/1024
##    ##                    FSflag += 1
##    ##                if FSflag == 1:
##    ##                    FSdisp = "Bytes"
##    ##                elif FSflag == 2:
##    ##                    FSdisp = "KB"
##    ##                elif FSflag == 3:
##    ##                    FSdisp = "MB"
##    ##                elif FSflag == 4:
##    ##                    FSdisp = "GB"
##                    File = open(w[6:],'wb')
##                    print("파일",w[6:],"수신")
##                    FScount = 0
##                    Fdata = s.recv(1024**2)
##                    while bytes("<End>\n",'utf-8') not in Fdata:
##                        FScount += len(Fdata)
##                        print("진행도:",FScount,"/",Fsize,FSdisp)
##                        File.write(Fdata)
##                        Fdata = s.recv(1024**2)
##                    File.write(Fdata[:-5])
##                    File.close()
##                    print("파일 수신 완료")
                
Reciever = Network()
Interface = App()
