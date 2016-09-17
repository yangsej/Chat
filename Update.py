import threading
from tkinter import *
import socket               # Import socket module
import time
import re


s = socket.socket()         # Create a socket object
host = 'Gibbs.server.ne.kr' # Get local machine name
port = 25565                # Reserve a port for your service.

class App(threading.Thread):
    def run(self):
        root = Tk()
        root.title("업데이트")
        root.geometry("600x400")
        root.minsize(600,400)
        root.maxsize(600,400)
        
        self.logframe = Frame(root)
        self.logframe.pack(expand=True, fill=BOTH,)
        
        self.log = Text(self.logframe)
        self.scrollbar = Scrollbar(self.logframe,command=self.log.yview)
        self.log.config(state="disabled", yscrollcommand=self.scrollbar.set)
        self.log.pack(expand=True, fill=BOTH, side=LEFT)
        self.scrollbar.pack(fill=Y, side=LEFT)

        root.mainloop()

    def logRefresh(self, msg):
        self.log.configure(state=NORMAL)
        flag=False
        if self.scrollbar.get()[1]>=0.95:
            flag=True
        self.log.insert(END, msg+'\n')
        if flag:
            self.log.yview_moveto(1)
            flag=False
        self.log.configure(state=DISABLED)

        

class Network(threading.Thread):
    def run(self):
        s.connect((host, port))
        s.send(bytes("<Updater>\n", 'utf-8'))
        while True:
            r = s.recv(1024)
            for w in Words:
                if w.startswith("<File>"):
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
                    print("업데이트 완료")


Interface = App()
Network = Network()

Interface.start()
Network.start()
