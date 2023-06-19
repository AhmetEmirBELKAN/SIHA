import requests
import time
import logging
import random
import numpy as np
import cv2
import json

from threading import Thread

from arayuz import YerIstasyonuArayuz
from logger import Logger
from kalman import IHAKalman
from tcplib import TCPServer
from camlib import IHAKamera

class YerIstasyonu:
    def __init__(self,takim_no,hakem_sunucu,iha_adres,login_bilgileri,kamera,arayuz_ws):
        self.logger=Logger()

        self.logger.log('YKI tanimlaniyor...',arayuze_gonder=False)

        self.logger.log('Sunucu bilgileri ayarlaniyor...',arayuze_gonder=False)

        self.set_sunucu_bilgileri(takim_no,hakem_sunucu,iha_adres,login_bilgileri,kamera,arayuz_ws)

        self.hakem_sunucu_endpointleri={
            "saat":"api/sunucusaati",
            "telemetri":"api/telemetri_gonder",
            "login":"api/login",
            "logout":"api/cikis"
        }
        self.hakem_sunucu_bagli=False

        self.telemetri_gonderim_periyot=600 #ms
        self.son_telemetri_gonderim=self.anlik_zaman

        self.logger.log('Sunucu bilgileri ayarlandi.',arayuze_gonder=False)

        # Kalman
        self.tkd={} # Takim kalman degiskenleri. Uzun yazmak zor geldi.
        self.yarisma_alani_noktalari={ # TODO: GUNCELLE
            'n1':{'lat':41.256983,'lon':36.554581},
            'n2':{'lat':41.256983,'lon':36.556313},
            'n3':{'lat':41.258351,'lon':36.556313},
            'n4':{'lat':41.258351,'lon':36.554581},
        }
        self.max_lat=max([n['lat'] for n in self.yarisma_alani_noktalari.values()])
        self.max_lon=max([n['lon'] for n in self.yarisma_alani_noktalari.values()])
        self.min_lat=min([n['lat'] for n in self.yarisma_alani_noktalari.values()])
        self.min_lon=min([n['lon'] for n in self.yarisma_alani_noktalari.values()])

        # Kamera
        self.kamera=IHAKamera(adres=self.kamera['udp']['adres'],port=self.kamera['udp']['port'], cozunurluk=kamera['cozunurluk'])

        # IHA
        # TODO: YKİ'de sunucuya gelen mesajlara gore işlem yapma
        self.iha_message_callback={
            'telemetri_al':self.telemetri_al,
        }
        self.iha_server=TCPServer(self.iha_adres['adres'],self.iha_adres['port'])
        
        # Arayuz
        self.arayuz_message_callback={
            'sunucu_bilgileri_guncelle':self.sunucu_bilgileri_guncelle,
            'goreve_basla':self.goreve_basla,
        }
        self.arayuz=YerIstasyonuArayuz(logger=self.logger)
        self.arayuz.start()

        self.running=False

        self.logger.log('YKI basariyla tanimlandi.')
    
    # Getters
    @property
    def anlik_zaman(self):
        return time.time()*1000
    
    @property
    def sunucu_saati(self):
        return requests.get(self.endpoint('saat')).json()

    def endpoint(self,endpoint:str):
        return f'{self.hakem_sunucu}/{self.hakem_sunucu_endpointleri[endpoint]}'

    # Hakem sunucu - Ucak ici bilgisayar iletisimi
    def set_sunucu_bilgileri(
        self,
        takim_no:str=None,
        hakem_sunucu:str=None,
        iha_adres:str=None,
        login_bilgileri:dict=None,
        kamera:dict=None,
        arayuz_ws:str=None
    ):
        # TODO: Buraya girdikten sonra tcp falan tekrar bağlantı kurmalı.
        if takim_no is not None:
            self.takim_no:str=takim_no
            self.logger.log(f'takim_no="{self.takim_no}"',arayuze_gonder=False)
        if hakem_sunucu is not None:
            self.hakem_sunucu:str=hakem_sunucu if not hakem_sunucu.endswith('/') else hakem_sunucu[:-1]
            self.logger.log(f'hakem_sunucu="{self.hakem_sunucu}"',arayuze_gonder=False)
        if iha_adres is not None:
            self.iha_adres:str=(iha_adres if not iha_adres.endswith('/') else iha_adres[:-1]).split(':')
            self.iha_adres={ # TODO: Burayı daha iyi bir şekilde çözebiliriz sanki
                'adres':self.iha_adres[0],
                'port':int(self.iha_adres[1])
            }
            self.logger.log(f'iha_adres={self.iha_adres}',arayuze_gonder=False)
        if login_bilgileri is not None:
            self.login_bilgileri:dict=login_bilgileri
            self.logger.log(f'login_bilgileri={self.login_bilgileri}',arayuze_gonder=False)
        if kamera is not None:
            self.kamera=kamera
            self.logger.log(f'kamera="{self.kamera}"',arayuze_gonder=False)
        if arayuz_ws is not None:
            self.arayuz_ws:str=arayuz_ws if not arayuz_ws.endswith('/') else arayuz_ws[:-1]
            self.logger.log(f'arayuz_ws="{self.arayuz_ws}"',arayuze_gonder=False)

    def set_hakem_sunucu_bagli(self,val:bool):
        self.hakem_sunucu_bagli=val
        self.arayuz.send('hakem_sunucu_bagli',val)

    def login(self):
        self.set_hakem_sunucu_bagli(False)
        self.logger.log('Hakem sunucuya baglaniliyor.')
        while True:
            try:
                login_response=requests.post(self.endpoint('login'),json=self.login_bilgileri)
                if login_response.status_code!=200:
                    self.logger.log(
                        'Hakem sunucuya giris yapilamadi ! Giris bilgileri:',
                        self.login_bilgileri,
                        f'Hakem sunucu yaniti: {login_response.status_code}',
                        '5 saniye sonra ayni bilgilerle tekrar giris denenecek.',
                        log_level=logging.ERROR
                    )
                    time.sleep(5)
                else:
                    self.logger.log('Hakem sunucuya giris yapildi.')
                    self.set_hakem_sunucu_bagli(True)
                    break
            except Exception as e:
                self.logger.log(f'Hakem sunucuya baglanilirken hata alindi! Hata: "{e}", 5 saniye sonra tekrar denenecek.',log_level=logging.ERROR)
                time.sleep(5)
    
    def telemetri(self):
        telemetri_verisi=self.telemetri_al()
        telemetri_yanit=self.telemetri_gonder(telemetri_verisi)
        if telemetri_yanit is not None:
            self.logger.log('Hakem sunucudan telemetri paketleri alindi.')
            # Thread(target=self.kalman_hesapla,args=(telemetri_yanit,)).start()
            self.son_telemetri_gonderim=self.anlik_zaman
            self.kalman_hesapla(telemetri_yanit)
        else:
            self.logger.log('Telemetri verisi alinamadi! Kalman hesaplamasi yapilamiyor.',log_level=logging.ERROR)
    
    # TODO: TCP TAMAMLANDIGINDA TEKRAR YAZILACAK
    def telemetri_al(self):
        response=requests.get(f'{self.iha_adres}/telemetri') # TODO: BURASI TCP
        telemetri_verisi=response.json()
        return telemetri_verisi
    
    def telemetri_gonder(self,telemetri_verisi:dict):
        # log('Telemetri verisi gonderiliyor..')
        # todo: son tel gon set
        telemetri_verisi.update({ # TODO: Gelen veriler işlenince oturucak değerler
            'takim_numarasi':self.takim_no,
            'GPSSaati':self.sunucu_saati,
            'IHA_otonom':1,
            'IHA_kitlenme':1,
            'Hedef_merkez_X':1.1,
            'Hedef_merkez_Y':1.1,
            'Hedef_genislik':1.1,
            'Hedef_yukseklik':1.1,
        })
        response=requests.post(self.endpoint('telemetri'),json=telemetri_verisi)
        if response.status_code==200:
            self.logger.log('Telemetri verisi gonderildi:',telemetri_verisi)
            return response.json()
        else:
            self.logger.log('Telemetri verisi gonderilemedi! Hakem sunucu yaniti: ',response.status_code,log_level=logging.ERROR)
            return None
    
    def logout(self):
        requests.get(self.endpoint('logout'))
        self.logger.log('Hakem sunucudan cikildi.')
    
    # Kalman - harita
    # TODO: Harita için uydu goruntusu kullanilabilir.

    def lat_lon_normalize(self,lat,lon):
        lat=(lat-self.min_lat)/(self.max_lat-self.min_lat)
        lon=(lon-self.min_lon)/(self.max_lon-self.min_lon)

        return lat,lon

    def takim_renk_kodu_ata(self):
        return (random.randint(50,255),random.randint(50,255),random.randint(50,255))
    
    # TODO: Kalmani tekrar incelemek gerekebilir.
    def kalman_hesapla(self,telemetri_yanit):
        takim_konumlari=telemetri_yanit['konumBilgileri']
        tahminler={}
        for tk in takim_konumlari:
            takim_no=tk['takim_numarasi']
            lat=tk['IHA_enlem']
            lon=tk['IHA_boylam']
            lat,lon=self.lat_lon_normalize(lat,lon)
            if takim_no not in self.tkd:
                self.tkd[takim_no]={
                    'kalman':IHAKalman(lat,lon),
                    'renk_kodu':self.takim_renk_kodu_ata(),
                }
            else:
                kalman:IHAKalman=self.tkd[takim_no]['kalman']
                kalman.koordinat_ekle(lat,lon)
                tahmin=kalman.tahmin()
                if tahmin!=None:
                    tahminler[takim_no]=tahmin
                    
        # TODO: Burdan sonrasi arayuzde islenecek
        # harita=np.zeros((self.harita_boy,self.harita_en,3),np.uint8)
        # for takim_no in tahminler.keys():
        #     renk_kodu=self.tkd[takim_no]['renk_kodu']
        #     for i in range(len(tahminler[takim_no]['lat'])-1):
        #         lat=int(tahminler[takim_no]['lat'][i]*self.harita_en)
        #         lon=int(tahminler[takim_no]['lon'][i]*self.harita_boy)
        
        #         yeni_lat=int(tahminler[takim_no]['lat'][i+1]*self.harita_en)
        #         yeni_lon=int(tahminler[takim_no]['lon'][i+1]*self.harita_boy)

        #         cv2.arrowedLine(harita,(lat,lon),(yeni_lat,yeni_lon),renk_kodu,1,tipLength=0.2)


    # Arayuz
    # Arayuzden gelen mesajlari isler.
    def arayuz_mesajlari_isle(self):
        for msg in self.arayuz.arayuz_messages():
            try:
                msg:dict=json.loads(msg)
            except json.decoder.JSONDecodeError:
                self.logger.log(f"Arayuzden gelen mesaj JSON'a dönüştürülemedi: {msg}",log_level=logging.ERROR)
                continue

            msg_type=msg.get('type',None)
            msg_func=self.arayuz_message_callback.get(msg_type,None)
            if not msg_func:
                self.logger.log(f'Bilinmeyen mesaj tipi: {msg_type}',log_level=logging.ERROR)
                return
            
            return_val=msg_func(msg['data'])
            
    def sunucu_bilgileri_guncelle(self,data):
        self.logger.log(f'Sunucu bilgileri guncelleniyor: {data}')
        
        self.set_sunucu_bilgileri(**data)
        with open('sunucu_bilgileri.json','w',encoding='utf8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)

        self.logger.log(f'Sunucu bilgileri guncellendi: {data}')

        return True

    # Gorev baslatma
    def goreve_basla(self,data):
        self.logger.log('IHA baslatma komutu alindi, IHA baslatiliyor...')
        # self.login()

        # TODO: Kamera icin gerekirse setup

        self.running=True

    # Ana metod
    def start(self):
        # self.iha_server.start()
        self.kamera.start()

        while True:
            if self.arayuz.is_connected: # Websocket baglanti kosulu.
                self.arayuz_mesajlari_isle()
            
            if self.running:
                try:
                    # Telemetri
                    # if self.anlik_zaman>self.son_telemetri_gonderim+self.telemetri_gonderim_periyot:
                    #     self.son_telemetri_gonderim=self.anlik_zaman
                    #     # self.telemetri() # Debug için commentte. Telemetri tamamlandığında açılacak.
                    
                    frame=self.kamera.frame
                    base64_frame = self.kamera.base64_frame
                    # print(frame)
                    # base64_frame=f'data:image/png;base64,{self.kamera.base64_frame}'
                    self.arayuz.send('kamera',base64_frame)

                    with open('base64.txt','w',encoding='utf8') as f:
                        f.write(base64_frame)
                
                except Exception as e:
                    self.logger.log('Hata!',e,log_level=logging.ERROR)
        
    # Gorev durdurma metodu
    def gorevi_durdur(self):
        pass