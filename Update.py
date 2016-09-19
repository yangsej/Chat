import threading
from tkinter import *
from tkinter import ttk
import socket               # Import socket module
import time
import re

from os import getcwd, system, remove
import zipfile
import subprocess

import Client


class App(threading.Thread):
    def run(self):
        root = Tk()
        root.title("업데이트")
        
        self.logframe = Frame(root)
        self.logframe.pack(expand=True, fill=BOTH,)
        
##        self.log = Text(self.logframe)
##        self.scrollbar = Scrollbar(self.logframe,command=self.log.yview)
##        self.log.config(state="disabled", yscrollcommand=self.scrollbar.set)
##        self.log.pack(expand=True, fill=BOTH, side=LEFT)
##        self.scrollbar.pack(fill=Y, side=LEFT)
        self.progress_name = StringVar(value="수신 대기중...")
        self.progress_label = Label(self.logframe, textvariable=self.progress_name)
        self.progress_label.pack(side=LEFT)
        
        
        self.progress_size_label = Label(self.logframe)
        self.progress_max_label = Label(self.logframe)
        self.progress_max_label.pack(side=RIGHT)
        self.progress_size_label.pack(side=RIGHT)

        self.progress_bar = ttk.Progressbar(root)
        self.progress_bar.pack(fill=X, side=BOTTOM)

        root.mainloop()


    def set_init(self, name, max):
        self.set_name(name)
        self.progress_size = IntVar()
        self.progress_size_label.config(textvariable=self.progress_size)
        self.progress_max_label.config(text=" / %s %s"%(max, "Bytes"))
        self.progress_bar.config(maximum=max)
        
    def progress(self, data_size):
        self.progress_size.set(self.progress_size.get()+data_size)
        self.progress_bar.step(data_size)

    def set_name(self, name):
        self.progress_name.set(name)
##    def set_progress(self, )
        

class Network(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.socket = socket.socket()
        host = 'Gibbs.server.ne.kr'
        port = 25565
        self.socket.connect((host, port))
        
    def run(self):
        self.socket.send(bytes("<Update><End_Update>\n", 'utf-8'))
        while True:
            recv = self.socket.recv(1024)
            Words = recv.split(b'\n')
            for i in range(len(Words)):
                if Words[i].startswith(b"<File>"):
                    if Words[i].endswith(b"<End_File>"):
                        file_name = Words[i][6:Words[i].rfind(b"<End_File>")].decode()
                        file = open(file_name,'wb')
                        
                elif Words[i].startswith(b"<Size>"):
                    if Words[i].endswith(b"<End_Size>"):
                        file_size = Words[i][6:Words[i].rfind(b"<End_Size>")].decode()
                        size_disp = "Bytes"
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

                        size_count = 0
                elif Words[i].startswith(b"<Data>"):
                    Interface.set_init("수신중: "+file_name, file_size)
                    
                    data=bytes()
                    for j in range(i+1, len(Words)):
                        data += Words[j]
                        if j+1 < len(Words):
                            data += b'\n'
                    while b"<End_Data>" not in data:
                        file.write(data)
                        size_count += len(data)
                        Interface.progress(len(data))

                        data = self.socket.recv(1024)
                        
                    file.write(data[:data.rfind(b"\n<End_Data>\n")])
                    size_count += len(data[:data.rfind(b"\n<End_Data>\n")])
                    Interface.progress(len(data[:data.rfind(b"\n<End_Data>\n")]))
                    file.close()
                    self.socket.close()

                    if zipfile.is_zipfile(file_name):
                        Interface.set_name("압축 해제중...")
                        self.unzip(file_name, getcwd())
                        
                    Interface.set_name("업데이트 완료")
                    remove("Client.zip")
                    time.sleep(1)
                    subprocess.Popen(["Client.exe"])
                    system("taskkill.exe /f /im Update.exe")
                    return
                    
                    
    def unzip(self, file_name, file_path=getcwd()):
        zf = zipfile.ZipFile(file_name, 'r')
        result = zf.extractall(path=file_path)
        zf.close()


Interface = App()
Network = Network()


Interface.start()
Network.start()
