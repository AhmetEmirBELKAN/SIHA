import json

from yer_istasyonu import YerIstasyonu

def main():
    with open('sunucu_bilgileri.json','r',encoding='utf8') as f:
        sunucu_bilgileri=json.load(f)
    
    yer_istasyonu=YerIstasyonu(**sunucu_bilgileri)
    yer_istasyonu.goreve_basla(None)
    yer_istasyonu.start()

if __name__=='__main__':
    main()

"""
TODO
- Arayüz resimlerini ilet
- Frontende websocket
- Sunucu bilgileri ayarla ilgili yere
- Logger'ı tekrardan yaz
"""