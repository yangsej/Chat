import socket
import threading
import time
from os import listdir
import pyaudio
import wave
import re

version = "0.01.001"

users=[]
updatelist = listdir("C:\\Users\\ysj\\Desktop\\python\\ChatClient")


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.socket = socket.socket()
        host = socket.gethostname()
        port = 25565
        self.socket.bind((host, port))
        
        print("========== Server Started ==========")
        
    def run(self):
        self.socket.listen(5)
        while True:
            netInfo = self.socket.accept()
            users.append(User(netInfo))
            users[-1].start()
##            recv = netInfo[0].recv(128)
##            recv_de = recv.decode()
##            recv_re = re.search("\<(\w+)\>(.*)\<(End\w*)\>\n", recv_de)
##            mode1 = recv_re.group(1)
##            instance = recv_re.group(2)
##            mode2 = recv_re.group(3)
##
##            print(mode1, instance, mode2)
            


class User(threading.Thread):
    def __init__(self, netInfo):
        threading.Thread.__init__(self)

        self.socket = netInfo[0]
        self.address = netInfo[1]
        self.name = ""
        self.version = ""

    def __str__(self):
        return self.name
      
    def run(self):
        try:
            

            ##         call(self.user)
            ##         self.filesend("2015_11_05_0002.jpg")
            while True:
                recv = self.socket.recv(1024)
                recv_de = recv.decode()
                print(repr(recv_de)) # 디버깅용
                recv_re = re.search("<(\w+)>(.*)<(End\w*)>\n", recv_de, re.DOTALL)
                mode1 = recv_re.group(1)
                instance = recv_re.group(2)
                mode2 = recv_re.group(3)
                print(mode1, instance, mode2) # 디버깅용
                
                if mode1 == "Version":
                    self.version = instance
                    self.socket.send(bytes("<Version>"+version+"<End_Version>\n",'utf-8'))
                elif mode1 == "Login":
                    self.name = instance
                    for u in users:
                        u.socket.send(bytes("<Login>"+self.name+"<End_Login>\n", "utf-8"))
                        if u.name != self.name:
                            self.socket.send(bytes("<Name>"+u.name+"<End_Name>\n", "utf-8"))
                        print(self.name, "님이 접속하셨습니다.", self.address, "|| Version:", self.version)
                elif mode1 == "Msg":
                    print(self.name+": "+instance)
                    for u in users:
                        u.socket.send(bytes('<'+mode1+'>'+self.name+": "+instance+'<'+mode2+'>\n','utf-8'))
                
               
        except ConnectionResetError:
            self.socket.close()
            outmsg=self.name+" 님이 퇴장하셨습니다."
            outip=self.address
            for u in users:
                if u.address == self.address:
                    users.remove(u)
                    break
            print(outmsg, outip)
            if users:
                for u in users:
                    u.socket.send(bytes("<Logout>"+self.name+"<End_Logout>\n",'utf-8'))

         
class File_Send(threading.Thread):
    def run(self):
        time.sleep(1)
        Fsize = os.path.getsize(Fname)
        File = open(Fname,'rb')
        print("파일 전송:",Fname,Fsize,self.user.name,self.user.addr)
        self.user.sock.send(bytes("<File>"+Fname+"\n<Size>"+str(Fsize)+"\n","utf-8"))
        Fdata = File.read(1024**2)
        time.sleep(1)
        while Fdata:
            self.user.sock.send(Fdata)
            Fdata = File.read(1024**2)
        time.sleep(1)
        self.user.sock.send(bytes("<End>\n",'utf-8'))
        File.close()
        print("전송 완료")
               
####class call(threading.Thread):
####    def __init__(self,user):
####        threading.Thread.__init__(self)
####        self.user = user
####        self.start()
####        
####    def run(self):
####        try:
####            self.wavesend()
####        except:
####            self.user.sock.close()
####            outmsg=self.user.name+" 님이 퇴장하셨습니다."
####            outip=self.user.addr
####            users.remove(self.user)
####            print(outmsg,outip)
####            if users:
####                for u in users:
####                u.sock.send(bytes("<Out>"+self.user.name+"\n",'utf-8'))
####            self.user.sock.close()
####    def wavesend(self):
####        if users:
####            for u in users:
####                u.sock.send(bytes("<Voice>\n",'utf-8'))
####                time.sleep(1)
####            CHUNK = 1024
####            FORMAT = pyaudio.paInt16
####            CHANNELS = 2
####            RATE = 44100
####            WAVE_OUTPUT_FILENAME = "output.wav"
####
####            p = pyaudio.PyAudio()
####
####            istream = p.open(format=FORMAT,
####                             channels=CHANNELS,
####                             rate=RATE,
####                             input=True,
####                             frames_per_buffer=CHUNK)
####      
####            while True:
####                data = istream.read(CHUNK)
####                if users:
####                    for u in users:
####                        u.sock.send(data)
####      if users:
####         for u in users:
####            u.sock.send(bytes("<End>\n",'utf-8'))
##      File = open(Fname,'rb')
##      print("파일 전송:",Fname,Fsize,self.user.name,self.user.addr)
##      self.user.sock.send(bytes("<File>"+Fname+"\n<Size>"+str(Fsize)+"\n","utf-8"))
##      Fdata = File.read(1024**2)
##      time.sleep(1)
##      while Fdata:
##         self.user.sock.send(Fdata)
##         Fdata = File.read(1024**2)
##      time.sleep(1)
##      self.user.sock.send(bytes("<End>\n",'utf-8'))
##      File.close()
##      print("전송 완료")
      
Sthread = Server()
Sthread.start()
