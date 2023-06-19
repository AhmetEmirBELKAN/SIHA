import socket
import cv2
import threading
import numpy as np
from io import BytesIO
import base64

class IHAKameraServer:
    def __init__(self,adres:str,port:int,cozunurluk:dict,cam_port=-1) -> None:
        self.adres=adres
        self.port=port
        self.cam_port=cam_port

        self.thread=None
        self.socket=None

        self.yki_adres=None

        self.running=False

        self.buff_size=65536
        self.cozunurluk=cozunurluk
    
    def connect(self):
        # TODO: Buraya şifreli bir mesaj gönderip ona göre bağlantı kabul edilebilir.
        # YKI adresini burada alırız.
        message,self.yki_adres = self.socket.recvfrom(self.buff_size)
        print(self.yki_adres)
        
    def setup(self):
        self.socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.adres,self.port))
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,self.buff_size)

        self.camera=cv2.VideoCapture(self.cam_port)

        self.connect()
    
    def send(self,frame:np.ndarray):
        frame=cv2.resize(frame,(self.cozunurluk['en'],self.cozunurluk['boy']))
        success,buffer=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        if success:
            frame=base64.b64encode(buffer)
            self.socket.sendto(frame,self.yki_adres)

    def run(self):
        while self.running:
            result, frame = self.camera.read()
            if result:
                self.send(frame)


    def start(self):
        self.setup()
        self.running=True
        self.thread=threading.Thread(target=self.run)
        self.thread.start()
    
    def stop(self):
        self.running=False
        # TODO: Durdurmak için gerekli adımlar
        pass

if __name__=='__main__':
    import json
    with open('iha_bilgileri.json','r') as f:
        iha_bilgileri=json.load(f)
    adres=iha_bilgileri['iha_udp']['adres']
    port=iha_bilgileri['iha_udp']['port']
    cozunurluk=iha_bilgileri['cozunurluk']
    server=IHAKameraServer(adres,port,cozunurluk)
    server.start()