from fastapi import FastAPI,Body,Response
from datetime import datetime
from iha_simulasyon import iha_simule_et

# sudo apt install uvicorn # Uvicorn indirmek gerekli çalıştırmak için
# python -m uvicorn hakem_sunucu:app --reload --port 5555 # Çalıştırma komutu - venv açık olan terminalden çalıştır
app =FastAPI()

LOGGED_IN=False
KULLANICI_ADI='ROKO'
SIFRE='BASILISK'

YARISMA_ALANI={
    'sol_alt':{'lat':41.256983,'lon':36.554581},
    'sag_ust':{'lat':41.258351,'lon':36.556313},
}

# 10 tane takım var. Onların anlık telemetri verilerini tutacak değişken.
TAKIM_TELEMETRI={i:None for i in range(1,16)}

def arasinda(val:int,d1:int,d2:int):
    return val>=d1 and val<=d2

def takim_telemetrileri():
    global TAKIM_TELEMETRI

    # Simulasyonu nasıl yaparız ? Ne şekilde bir mantıkla yaklasmamız lazım ?
    for takim in TAKIM_TELEMETRI.keys():
        telemetri=iha_simule_et(TAKIM_TELEMETRI[takim])
        telemetri['takim_numarasi']=takim
        TAKIM_TELEMETRI[takim]=telemetri

    return list(TAKIM_TELEMETRI.values())

@app.post('/api/login')
def login(creds:dict=Body(...)):
    global LOGGED_IN,KULLANICI_ADI,SIFRE
    kullanici_adi=creds.get('kadi',None)
    sifre=creds.get('sifre',None)
    if kullanici_adi==KULLANICI_ADI and sifre==SIFRE:
        LOGGED_IN=True
        return Response(status_code=200)
    return Response(status_code=400)

@app.get('/api/cikis')
def logout():
    global LOGGED_IN
    LOGGED_IN=False

@app.get('/api/sunucusaati') #end point
def sunucu_saati():
    if not LOGGED_IN:
        return Response(status_code=401)

    an = datetime.now()
    saat=an.hour
    dakika=an.minute
    saniye=an.second
    milisaniye=an.microsecond

    return {
        'saat':saat,    
        "dakika":dakika,
        "saniye":saniye,
        "milisaniye":milisaniye
    }


@app.post('/api/telemetri_gonder')
def telemetri_bilgi(data:dict=Body(...)):
    if not LOGGED_IN:
        return Response(status_code=401)

    required_data_keys={
        "takim_numarasi":int,
        "IHA_enlem":float,
        "IHA_boylam":float,
        "IHA_irtifa":float,
        "IHA_dikilme":float,
        "IHA_yonelme":float,
        "IHA_yatis":float,
        "IHA_hiz":float,
        "IHA_batarya":float,
        "IHA_otonom":[0,1],
        "IHA_kitlenme":[0,1],
        "Hedef_merkez_X":float,
        "Hedef_merkez_Y":float,
        "Hedef_genislik":float,
        "Hedef_yukseklik":float,
        "GPSSaati":{
            "saat":int,
            "dakika":int,
            "saniye":int,
            "milisaniye":int,
        },
    }

    for key,data_type in required_data_keys.items():
        if key not in data:
            print(f"eksik anahtar:{key}")
            return Response(status_code=204)

        if isinstance(data_type,dict):
            for k,dt in required_data_keys[key].items():
                if not isinstance(data[key][k],dt):
                    print(f'hatalı veri: {key}.{k} değeri {dt} olmalı.')
                    return Response(status_code=204)
        
        elif isinstance(data_type,list):
            if data[key] not in data_type:
                print(f"hatalı veri: '{key}' değeri {data_type} olmalı")
                return Response(status_code=204)
        
        elif not isinstance(data[key],data_type):
            print(f"hatalı veri: '{key}' değeri {data_type} olmalı")
            return Response(status_code=204)

    return {
        "sistemSaati": sunucu_saati(),
        "konumBilgileri": takim_telemetrileri()
    }
