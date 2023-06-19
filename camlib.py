import socket
import numpy as np
import threading
import cv2
import base64

class IHAKamera:
    def __init__(self, adres:str, port:int, cozunurluk:dict): # TODO: Kamera bilgileri dict olsa daha iyi ama frontendde düzeltme gerekir.
        self.adres=adres
        self.port=port

        self.connected=False
        self.running=False

        self.cozunurluk=cozunurluk

        self.frame=np.arange(self.cozunurluk['en']*self.cozunurluk['boy']*3).reshape((self.cozunurluk['en'],self.cozunurluk['boy'],3))
        # self.frame=None
        self.buff_size=65536
        # self.frame_lock=threading.Lock() # GIL olduğundan lock koymadım. En kötü ihtimalde bir frame öncesini alır. Performans kaybetmektense onun olması daha iyi.
    
    @property
    def base64_frame(self):
        if self.frame is None:
            return None
        
        return base64.b64encode(cv2.imencode('.jpg', self.frame)[1]).decode()

    def connect(self):
        # Burada kameraya kendi adresimizi gönderiyoruz aslında.
        # TODO: Buraya şifreli bir mesaj gönderilebilir, başkası bağlanmak isterse önüne geçmiş oluruz.
        while True:
            self.socket.sendto(b'hello',(self.adres,self.port))
            # try: # Şifreli yaparsak karşıdan da yanıt gelmesi gerek.
            #     self.socket.recvfrom(self.buff_size)
            # except TimeoutError:
            #     continue
            self.connected=True
            break

    def setup(self):
        self.socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)
        self.socket.bind(("",30001)) # Portun tekrar bağlanma gerektirmemesi için sürekli aynı olması gerekiyor.
        self.connect()

    def decode(self,frame_buffer:bytes):
        # base64_frame=base64.b64encode(frame_buffer).decode('ascii')
        # frame_buffer = base64.b64decode(frame_buffer,' /')
        # decoded_frame = np.fromstring(frame_buffer,dtype=np.uint8)
        # frame = cv2.imdecode(decoded_frame,1)

        frame_buffer = base64.b64decode(frame_buffer.decode('ascii'))
        frame = np.frombuffer(frame_buffer, dtype=np.uint8)
        frame = cv2.imdecode(frame, flags=1)

        return frame

    def run(self):
        while self.running:
            if self.connected:
                try:
                    packet,_ = self.socket.recvfrom(self.buff_size,)
                except TimeoutError:
                    self.connected=False
                    continue
                self.frame=self.decode(packet)
                # self.base64_frame,self.frame=self.decode(packet)
                # print(self.frame)
                # cv2.imwrite('qwe.png',self.frame)
            else:
                self.connect()


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
    import time
    with open('sunucu_bilgileri.json','r') as f:
        sunucu_bilgileri=json.load(f)

    adres=sunucu_bilgileri['kamera_udp']['adres']
    port=sunucu_bilgileri['kamera_udp']['port']
    kamera=IHAKamera(adres=adres,port=port)
    kamera.start()
    while True:
        time.sleep(0.5)