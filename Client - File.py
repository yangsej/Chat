import threading
from tkinter import *
import socket
import time
import re
import os

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
        self.chat_text = Text(self.frame, width=60, padx=2, pady=2, height=40, state="disabled")
        self.chat_text_scroll = Scrollbar(self.frame,command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=self.chat_text_scroll.set)
        self.chat_text.pack(side='left',fill='y')
        self.chat_text_scroll.pack(side='left',fill='y')

        #유저 리스트
        self.user_list = Listbox(self.frame)
        self.user_scroll = Scrollbar(self.frame,command=self.user_list.yview)
        self.user_list.configure(width=27,state="disabled", yscrollcommand=self.user_scroll.set)
        self.user_list.pack(side='left',fill='y')
        self.user_scroll.pack(side='left',fill='y')

        #전송 버튼
        send_image = PhotoImage(file='C:\\Users\\ysj\\Desktop\\python\\Networking\\gavel.gif')
        self.send_button = Button(self.frame2,image=send_image, command=self.send_MSG)
        self.send_button.pack()
        self.send_button.bind("<Return>",self.send_MSG)

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
        self.input_text.pack(side='bottom',fill='both')
        
        self.input_text.bind("<Return>",self.send_MSG)
        self.input_text.bind("<Shift-Return>",self.send_MSG)

        root.mainloop()
        
    def refresh(self, msg):
        self.MSGL.configure(state="normal")
        flag=0
        if self.scrollbar.get()[1]==1.0:
            flag=1
        self.MSGL.insert("end",msg+'\n')
        if flag==1:
            self.MSGL.yview_scroll(1,"units")
            flag=0
        self.MSGL.configure(state="disabled")
        
    def add_User(self,Uname):
        global users
        self.user_list.insert(END, Uname)
        users.append(Uname)
        
    def remove_User(self,Uname):
        global users
        self.UserL.configure(state="normal")
        for l in range(len(users)):
            if users[l]==Uname:
                line = float(l+1)
                break
        print(line)
        self.UserL.delete(line,line+1.0)
        self.UserL.configure(state="disabled")
        users.remove(Uname)
    
    def send_MSG(self, event=None):
        MSG = self.input_text.get(1.0,"end").strip()
        if MSG:
            Reciever.socket.send(bytes(MSG,'utf-8'))
        self.input_text.delete(0.0, END)
        
    def set_Volume(self,event):
        self.volume = self.volume_scale.get()     
        

class Network(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.socket = socket.socket()
        host = 'Gibbs.server.ne.kr'
        port = 25565
        self.socket.connect((host, port))
        print(name)
        self.socket.send(bytes("<Name>"+name+"<End_Name>\n",'utf-8'))

        self.start()

    def run(self):
        while True:
            recv = self.socket.recv(1024)
            r = recv.decode()
            Words = r.split("\n")
    ##        print(Words)
            for w in Words:
                if w.startswith("<Names>"):
                    Uname=''
                    while "<End>" not in Uname:
                        Uname += self.socket.recv(256).decode()
    ##                    print(Uname)
                    UNlist=Uname.split("\n")
    ##                print(UNlist)
                    for UN in UNlist:
                        if UN.startswith("<Name>"):
                            IApp.UserListA(UN[6:])
                        if UN.startswith("<End>"):
                            break
                if w.startswith("<Name>"):
                    Uname = w[6:]
                    IApp.UserListA(Uname)
                    IApp.logRefresh(Uname+' 님이 접속하셨습니다')
                elif w.startswith("<Out>"):
                    Uname = w[5:]
                    IApp.UserListS(Uname)
                    IApp.logRefresh(Uname+" 님이 퇴장하셨습니다.")
                elif w.startswith("<Msg>"):
                    Msg = w[5:]
                    IApp.logRefresh(Msg)
                elif w.startswith("<File>"):
                    Fsize = int(Words[1][6:])
                    FSdisp="Bytes"
    ##                FSflag = 1
    ##                while Fsize > 1024:
    ##                    Fsize = Fsize/1024
    ##                    FSflag += 1
    ##                if FSflag == 1:
    ##                    FSdisp = "Bytes"
    ##                elif FSflag == 2:
    ##                    FSdisp = "KB"
    ##                elif FSflag == 3:
    ##                    FSdisp = "MB"
    ##                elif FSflag == 4:
    ##                    FSdisp = "GB"
                    File = open(w[6:],'wb')
                    print("파일",w[6:],"수신")
                    FScount = 0
                    Fdata = s.recv(1024**2)
                    while bytes("<End>\n",'utf-8') not in Fdata:
                        FScount += len(Fdata)
                        print("진행도:",FScount,"/",Fsize,FSdisp)
                        File.write(Fdata)
                        Fdata = s.recv(1024**2)
                    File.write(Fdata[:-5])
                    File.close()
                    print("파일 수신 완료")
                    

Interface=App()
Reciever = Network()
