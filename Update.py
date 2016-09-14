import threading
import tkinter
import socket               # Import socket module
import time
import re


s = socket.socket()         # Create a socket object
host = 'Gibbs.server.ne.kr' # Get local machine name
port = 25565                # Reserve a port for your service.

F=tkinter.Frame
T=tkinter.Text
S=tkinter.Scrollbar
L=tkinter.Label
B=tkinter.Button
class App(threading.Thread):
    def run(self):
        master=tkinter.Tk()
        master.title("업데이트")
        master.geometry("600x600")
        self.frame = F(master)
        self.frame.pack(fill="both")

        self.frame1 = F(self.frame)
        self.frame1.pack(fill="both")
        
        self.MSGL = T(self.frame1,padx=1,pady=1)
        self.scrollbar = S(self.frame1,command=self.MSGL.yview)
        self.MSGL.configure(width=80, height=45, state="disabled", yscrollcommand=self.scrollbar.set)
        self.MSGL.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        master.mainloop()

        
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



def network():
    s.connect((host, port))
    s.send(bytes("<Updater>\n"))
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


IApp=App()
Nthread = threading.Thread(target = network)

IApp.start()
Nthread.start()
