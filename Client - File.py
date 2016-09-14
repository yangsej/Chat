import threading
import tkinter
import socket               # Import socket module
import time
import re
import os


s = socket.socket()         # Create a socket object
host = 'Gibbs.server.ne.kr' # Get local machine name
port = 25565                # Reserve a port for your service.
while True:
    name=str(input("닉네임 : "))
    if 2<=len(name)<=20:
        break
    else:
        print("닉네임은 2글자 이상이어야 합니다.")
users=[]

F=tkinter.Frame
T=tkinter.Text
S=tkinter.Scrollbar
L=tkinter.Label
B=tkinter.Button
Scale=tkinter.Scale
class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        root=tkinter.Toplevel()
        root.title("채팅")
        root.geometry("650x630")
        root.minsize(655,632)
        #root.maxsize(650,630)
        self.frame = F(root)
        self.frame.pack()
        
        self.frame1 = F(self.frame)
        self.frame1.pack(side='bottom',fill='x')
                
        self.frame2 = F(self.frame1)
        self.frame2.pack(side='right')

        self.frame3 = F(self.frame1)
        self.frame3.pack()

        self.MSGL = T(self.frame,width=60,padx=2,pady=2,height=40,state="disabled")
        self.scrollbar = S(self.frame,command=self.MSGL.yview)
        self.MSGL.configure(yscrollcommand=self.scrollbar.set)
        self.MSGL.pack(side='left',fill='y')
        self.scrollbar.pack(side='left',fill='y')

        self.UserL = T(self.frame,padx=2,pady=2)
        self.UScroll = S(self.frame,command=self.UserL.yview)
        self.UserL.configure(width=27,state="disabled", yscrollcommand=self.UScroll.set)
        self.UserL.pack(side='left',fill='y')
        self.UScroll.pack(side='left',fill='y')


        gavelImg = tkinter.PhotoImage(file='C:\\Users\\ysj\\Desktop\\python\\Networking\\gavel.gif')
        self.sendB = B(self.frame2,image=gavelImg,command=self.BClicked)
        self.sendB.pack()

        self.label = L(self.frame3, text="닉네임 : "+name)
        self.label.pack(side='left',anchor='w',padx=30,fill='x')

        self.volm = L(self.frame3, text='0')
        self.volm.pack(side='left',anchor='e')
        self.volume = 100
        self.volumeS = Scale(self.frame3,orient='horizontal',showvalue=0)
        self.volumeS.set(100)
        self.volumeS.configure(command=self.setVolume)
        self.volumeS.pack(side='left',anchor='e')
        self.volM = L(self.frame3, text='100')
        self.volM.pack(side='left',anchor='e')
        self.volumeS.bind('<ButtonRelease-1>',self.setVolume)
        
        self.input = T(self.frame1,height=6,padx=2,pady=2)
        self.input.pack(side='bottom',fill='both')
        
        self.input.bind("<Return>",self.BClickedE)
        self.input.bind("<Shift-Return>",self.Enter)
        self.sendB.bind("<Return>",self.BClickedE)

        root.mainloop()

        
    def logRefresh(self,msg):
        self.MSGL.configure(state="normal")
        flag=0
        if self.scrollbar.get()[1]==1.0:
            flag=1
        self.MSGL.insert("end",msg+'\n')
        if flag==1:
            self.MSGL.yview_scroll(1,"units")
            flag=0
        self.MSGL.configure(state="disabled")
##        print(self.scrollbar.config())
##        self.scrollbar.activate("arrow2")
##        self.scrollbar.set('hi')
    def BClicked(self):
        self.sendMSG()
    def BClickedE(self,event):
        self.sendMSG()
    def UserListA(self,Uname):
        self.UserL.configure(state="normal")
        self.UserL.insert("end",Uname+'\n')
        self.UserL.configure(state="disabled")
        users.append(Uname)
    def UserListS(self,Uname):
        self.UserL.configure(state="normal")
        for l in range(len(users)):
            if users[l]==Uname:
##                print("here")
                line = float(l+1)
                break
##        ind=self.UserL.get(1.0,'end').index(Uname)
##        print(ind,ind+len(Uname))
        print(line)
        self.UserL.delete(line,line+1.0)
        self.UserL.configure(state="disabled")
        users.remove(Uname)
    def Enter(self,event):
        pass
    def sendMSG(self):
        MSG = self.input.get(1.0,"end").strip()
        if MSG:
            s.send(bytes(MSG,'utf-8'))
        self.input.delete(1.0,"end")
    def setVolume(self,event):
        if event:
            self.volume=self.volumeS.get()     
        


def network():
    s.connect((host, port))
    s.send(bytes(name,'utf-8'))
    while True:
        r = s.recv(1024).decode()
        Words = r.split("\n")
##        print(Words)
        for w in Words:
            if w.startswith("<Names>"):
                Uname=''
                while "<End>" not in Uname:
                    Uname+=s.recv(256).decode()
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
                

IApp=App()

Nthread = threading.Thread(target = network)
##Ithread = threading.Thread(target = interface)
##Rthread = recieve()
##Sthread = send()

IApp.start()
Nthread.start()
##Ithread.start()
##Rthread.start()
##Sthread.start()
##interface()
