import socket
import threading
import json
import time

def json_to_bytes(data:dict):
    return bytes(json.dumps(data),'ascii')

class TCPConnection:
    def __init__(self,address:str,port:int):
        # Adres
        self.socket_address:tuple[str,int]=(address,port)
        
        # Socket objesi
        self.socket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Address in use hatası için

        # Bağlantı bilgisi
        self.client:socket.socket=None
        self.client_address=None
        
        self.listen_thread=None
        self.connect_lock=threading.Lock()
        self.connected=False

        self.listen_thread=threading.Thread(target=self.listen)
        self.listen_thread.start()

        self.response_lock=threading.Lock() # Veri gönderildiğinde alınır. Yanıt dönene kadar bekletir.

    # Bu çağrıldığında mesajlar dinlenir
    def listen(self):
        while True:
            if self.connected:
                print('before receive')
                self.handle(self.client.recv(1024))
                print('after receive')
            else:
                with self.connect_lock: # Bağlanana kadar bekletmek için. Bağlanırken bu lock kapatılır, bağlandığında açılır.
                    continue

    
    def handle(self,data:bytes):
        # TODO: Veri geldiğinde çalışacak kod parçası
        print('received data',data)
        if data==b'':
            self.connected=False
            self.start()
            return

        try:
            data=json.loads(data)
        except json.decoder.JSONDecodeError:
            response={'type':'invalid_data','data':data.decode('ascii')}
            self.send(json_to_bytes(response))
            return
        

    # Mesaj göndermek için
    def send(self,data:bytes):
        with self.connect_lock: # Bağlanana kadar bekletmek için. Bağlanırken bu lock kapatılır, bağlandığında açılır.
            pass
        print('sending data',data)
        self.client.send(data)
    
    def connect(self):
        raise NotImplementedError("Base class connect metodunu içermez")
    
    def start(self):
        with self.connect_lock:
            self.connect()
            self.connected=True

class TCPServer(TCPConnection):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.socket.bind(self.socket_address)

    def connect(self):
        self.socket.listen(1)
        self.client,self.client_address=self.socket.accept()

class TCPClient(TCPConnection):
    def connect(self):
        print('connect')
        self.client=socket.socket()
        while True:
            try:
                self.client.connect(self.socket_address)
                break
            except ConnectionRefusedError:
                time.sleep(0.5)
                
            

def main():
    import sys

    if len(sys.argv)<=1:
        print('Server (-s) veya client (-c) parametresi yok.-> python tcplib.py -s')
        return
        
    if sys.argv[1]=='-s':
        server=TCPServer('localhost',4567)
        server.start()
        import time
        while True:
            time.sleep(0.5)
            server.send(b'testdata')
    elif sys.argv[1]=='-c':
        client=TCPClient('localhost',4567)
        client.start()

        import time
        while True:
            time.sleep(0.5)
            client.send(b'testdata')
    else:
        print('İlk arguman server (-s) veya client (-c) olmalı -> python tcplib.py -s')

if __name__=='__main__':
    main()