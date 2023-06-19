import math
import random

YARISMA_ALANI={
    'sol_alt':{'lat':41.256983,'lon':36.554581},
    'sag_ust':{'lat':41.258351,'lon':36.556313},
}

M_LAT=(YARISMA_ALANI["sag_ust"]['lat']-YARISMA_ALANI["sol_alt"]['lat'])/500
M_LON=(YARISMA_ALANI["sag_ust"]['lon']-YARISMA_ALANI["sol_alt"]['lon'])/350
SANIYELIK_BATARYA_TUKETIMI=15*60/100 # 15 dakika uçar. Her saniye yüzdelik harcama.

def arasinda(val:int,d1:int,d2:int):
    return val>=d1 and val<=d2

def iha_simule_et(telemetri:dict):
    global M_LAT,M_LON,YARISMA_ALANI,SANIYELIK_BATARYA_TUKETIMI
    if telemetri is None:
        telemetri={
            "IHA_enlem": random.uniform(YARISMA_ALANI['sol_alt']['lat'],YARISMA_ALANI["sag_ust"]['lat']),
            "IHA_boylam": random.uniform(YARISMA_ALANI['sol_alt']['lon'],YARISMA_ALANI["sag_ust"]['lon']),
            "IHA_irtifa": random.uniform(10,100),
            "IHA_dikilme": random.uniform(-30,30),
            "IHA_yonelme": random.uniform(0,360),
            "IHA_hiz": random.uniform(30,60),
            "IHA_yatis": random.uniform(-10,10),
            "IHA_batarya":100.0,

            "zaman_farki": random.randint(50,500),
        }
    
    else:
        hiz_degisim=random.uniform(-1,1)
        hiz=telemetri['IHA_hiz']+hiz_degisim
        if hiz<30:
            hiz=30
        elif hiz>60:
            hiz=60

        ort_hiz=hiz+telemetri['IHA_hiz']/2
        telemetri['IHA_hiz']=float(hiz)

        zaman_farki=random.uniform(50,500)/1000

        aci=telemetri['IHA_yonelme']+random.uniform(-30,30)
        aci=360-aci if aci > 360 else aci
        aci=360+aci if aci<0 else aci
        telemetri['IHA_yonelme']=aci

        telemetri['IHA_yatis']=random.uniform(-10,10)
        telemetri['IHA_batarya']-=(zaman_farki/1000)*SANIYELIK_BATARYA_TUKETIMI
        telemetri['IHA_irtifa']+=random.uniform(-1,1)
        telemetri['IHA_dikilme']=random.uniform(-30,30)

        if telemetri['IHA_irtifa']<10:
            telemetri['IHA_irtifa']=10
        elif telemetri['IHA_irtifa']>100:
            telemetri['IHA_irtifa']=100

        x_degisim=0
        y_degisim=0

        konum_degisim=float(zaman_farki*ort_hiz)
        
        if aci==0: # Tam kuzeye bakıyo, hız direk yukarıya dogru
            y_degisim=konum_degisim
            
        elif aci==180:# Tam güney - aşağıya
            y_degisim=konum_degisim*(-1)

        elif aci==90: # Tam doğu - sağ
            x_degisim=konum_degisim

        elif aci==270: # Tam batı - sol
            x_degisim=konum_degisim*(-1)

        else:
            if arasinda(aci,0,90): # Açılı - hem x_degisim hem y_degisim degisecek
                aci=abs(90-aci)
                x_degisim=konum_degisim*math.cos(aci)
                y_degisim=konum_degisim*math.sin(aci)

            elif arasinda(aci,90,180):
                aci=aci-90
                x_degisim=konum_degisim*math.cos(aci)
                y_degisim=konum_degisim*math.sin(aci)*(-1)

            elif arasinda(aci,180,270):
                aci=abs(270-aci)
                x_degisim=konum_degisim*math.cos(aci)*(-1)
                y_degisim=konum_degisim*math.sin(aci)*(-1)

            elif aci>270:
                aci=abs(360-aci)
                x_degisim=konum_degisim*math.cos(aci)*(-1)
                y_degisim=konum_degisim*math.sin(aci)
            
        telemetri['IHA_enlem']+=x_degisim*M_LAT
        telemetri['IHA_boylam']+=y_degisim*M_LON
    
    return telemetri