import socket
import threading
import time
import os
import pyaudio
import wave

s = socket.socket()
host = socket.gethostname()
port = 25565
s.bind((host, port))
users=[]
updatelist = os.listdir("C:\\Users\\ysj\\Desktop\\python\\ChatClient")

class user():
   def __init__(self,netInfo,name):
      self.sock = netInfo[0]
      self.addr = netInfo[1]
      self.name = name
      self.thread = None

class server(threading.Thread):
   def run(self):
      print("Server Started")
      s.listen(5)
      while True:
         netInfo = s.accept()
         name = netInfo[0].recv(128).decode()
         users.append(user(netInfo, name))
         users[-1].sock.send(bytes("<Names>\n",'utf-8'))
         for u in users:
            users[-1].sock.send(bytes("<Name>"+u.name+"\n",'utf-8'))
            if u.name!=name:
               u.sock.send(bytes("<Name>"+name+"\n",'utf-8'))
         users[-1].sock.send(bytes("<End>\n",'utf-8'))
            
         users[-1].thread = chat(users[-1])
         print(name,"님이 접속하셨습니다",users[-1].addr)


class chat(threading.Thread):
   def __init__(self,user):
      threading.Thread.__init__(self)
      self.user = user
      self.start()
   def run(self):
      try:
         call(self.user)
##         self.filesend("2015_11_05_0002.jpg")
         while True:
            r=self.user.sock.recv(1024).decode()
            msg='<Msg>'+self.user.name+": "+r+"\n"
            print(msg)
            for u in users:
               u.sock.send(bytes(msg,'utf-8'))
      except:
         self.user.sock.close()
         outmsg=self.user.name+" 님이 퇴장하셨습니다."
         outip=self.user.addr
         users.remove(self.user)
         print(outmsg,outip)
         if users:
            for u in users:
               u.sock.send(bytes("<Out>"+self.user.name+"\n",'utf-8'))
         self.user.sock.close()
         
   def filesend(self,Fname):
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
               
class call(threading.Thread):
   def __init__(self,user):
      threading.Thread.__init__(self)
      self.user = user
      self.start()
   def run(self):
      try:
         self.wavesend()
      except:
         self.user.sock.close()
         outmsg=self.user.name+" 님이 퇴장하셨습니다."
         outip=self.user.addr
         users.remove(self.user)
         print(outmsg,outip)
         if users:
            for u in users:
               u.sock.send(bytes("<Out>"+self.user.name+"\n",'utf-8'))
         self.user.sock.close()
   def wavesend(self):
      if users:
         for u in users:
            u.sock.send(bytes("<Voice>\n",'utf-8'))
         time.sleep(1)
      CHUNK = 1024
      FORMAT = pyaudio.paInt16
      CHANNELS = 2
      RATE = 44100
      WAVE_OUTPUT_FILENAME = "output.wav"

      p = pyaudio.PyAudio()

      istream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
      
      while True:
          data = istream.read(CHUNK)
          if users:
            for u in users:
               u.sock.send(data)
      if users:
         for u in users:
            u.sock.send(bytes("<End>\n",'utf-8'))
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
      
Sthread = server()
Sthread.start()
