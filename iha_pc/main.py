from camserver import IHAKameraServer
from multiprocessing import Process
import time

class IHA:
    def __init__(self, kamera_adres:str,kamera_port:int,cozunurluk:dict):
        # Kamera Server
        self.kamera_server=IHAKameraServer(adres=kamera_adres,port=kamera_port,cozunurluk=cozunurluk)

    
    def start_kamera_server(self):
        # TODO: Duruma göre subprocess yapılabilir
        self.kamera_server_process=Process(target=self.kamera_server.start)
        self.kamera_server_process.start()
    
    def run(self):
        self.start_kamera_server()
        while True:
            time.sleep(0.5)

def main():
    import json
    with open('iha_bilgileri.json','r') as f:
        iha_bilgileri=json.load(f)
    
    adres=iha_bilgileri['kamera_udp']['adres']
    port=iha_bilgileri['kamera_udp']['port']
    cozunurluk=iha_bilgileri['cozunurluk']

    iha = IHA(kamera_adres=adres,kamera_port=port,cozunurluk=cozunurluk)

    iha.run()

if __name__=='__main__':
    main()