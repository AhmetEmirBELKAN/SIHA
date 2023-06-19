<template>
  <!-- <div class="container">
    <div class="bilgiler-kamera-kalman">
      <div class="bilgiler">
        <div class="baglanti-bilgileri">
          <h2>BAĞLANTI BİLGİLERİ</h2>
          <div class="bilgi-satir">
            <h4>Yer istasyonu:</h4>
            <p :style="{color:yerIstasyonuBagli ? 'green' : 'red'}">{{yerIstasyonuBagli ? 'Bağlandı' : 'Bağlı değil'}}</p>
          </div>
          <div class="bilgi-satir">
            <h4>Hakem sunucu:</h4>
            <p :style="{color:hakemSunucuBagli ? 'green' : 'red'}">{{hakemSunucuBagli ? 'Bağlandı' : 'Bağlı değil'}}</p>
          </div>
          <div class="bilgi-satir">
            <h4>IHA bağlantı:</h4>
            <p>{{ihaDurum}}</p>
          </div>
          <div class="bilgi-satir">
            <h4>Yarışma süresi:</h4>
            <p>{{yarismaSuresi}}</p>
          </div>
        </div>
        <div class="sunucu-bilgileri">
          <h2>SUNUCU BİLGİLERİ</h2>
          <div class="bilgi-satir">
            <h4>Takım numarası:</h4>
            <input type="text" v-model="sunucuBilgileri.takim_no">
          </div>
          <div class="bilgi-satir">
            <h4>Hakem sunucu:</h4>
            <input type="text" v-model="sunucuBilgileri.hakem_sunucu">
          </div>
          <div class="bilgi-satir">
            <h4>IHA adres:</h4>
            <input type="text" v-model="sunucuBilgileri.iha_adres">
          </div>
          <div class="bilgi-satir">
            <h4>Kullanıcı adı:</h4>
            <input type="text" v-model="sunucuBilgileri.login_bilgileri.kadi">
          </div>
          <div class="bilgi-satir">
            <h4>Şifre:</h4>
            <input type="text" v-model="sunucuBilgileri.login_bilgileri.sifre">
          </div>
          <Button label="Kaydet" icon="pi pi-save" class="p-button-success" @click="ykiSunucuBilgileriGuncelle()"></Button>
        </div>
      </div>
      <div class="bilgiler">
        <div class="gorev-bilgileri">
          <h2>GÖREV BİLGİLERİ</h2>
          <div class="bilgi-satir">
            <h4>Yarışma süresi:</h4>
            <p>00:00</p>
          </div>
          <div class="bilgi-satir">
            <h4>Son kitlenilen takım:</h4>
            <p>156879</p>
          </div>
          <div class="bilgi-satir">
            <h4>Kitlenilen IHA sayısı:</h4>
            <p>5</p>
          </div>
          <div class="bilgi-satir">
            <h4>Kamikaze görevi:</h4>
            <p>Yapıldı</p>
          </div>
        </div>
        <div class="gorev-bilgileri">
          <h2>HIZLI KOMUTLAR</h2>
          <div class="bilgi-satir">
            <Button label="Göreve başla" class="p-button-text p-button-sm" :disabled="!yerIstasyonuBagli" @click="goreviBaslat()"></Button>
          </div>
          <div class="bilgi-satir">
            <Button label="Görevi duraklat" class="p-button-text p-button-sm"></Button>
          </div>
          <div class="bilgi-satir">
            <Button label="Görevi tamamla" class="p-button-text p-button-sm"></Button>
          </div>
          <div class="bilgi-satir">
            <Button label="Otonom iniş" class="p-button-text p-button-sm"></Button>
          </div>
          <div class="bilgi-satir">
            <Button label="Eve dönüş" class="p-button-text p-button-sm"></Button>
          </div>
        </div>
      </div>
      <div class="kamera-ibreler-kalman">
        <div class="kamera-kalman">
          <img id="kamera" :width="sunucuBilgileri.kamera.cozunurluk.en" :height="sunucuBilgileri.kamera.cozunurluk.boy">
          <canvas id="kalman-harita-canvas" :width="sunucuBilgileri.kamera.cozunurluk.en" :height="sunucuBilgileri.kamera.cozunurluk.boy"></canvas>
        </div>
        <div class="ibreler">
          <canvas id="hiz-gosterge" :width="ibreBoyutlari.en" :height="ibreBoyutlari.boy"></canvas>
          <canvas id="irtifa-gosterge" :width="ibreBoyutlari.en" :height="ibreBoyutlari.boy"></canvas>
          <canvas id="pitch-yaw-gosterge" :width="ibreBoyutlari.en" :height="ibreBoyutlari.boy"></canvas>
          <canvas id="pusula-gosterge" :width="ibreBoyutlari.en" :height="ibreBoyutlari.boy"></canvas>
        </div>
      </div>
    </div>
    <div id="logtable">
      <DataTable :value="logList" :scrollable="true" scrollHeight="380px" tableStyle="{'width':'auto'}">
        <Column field="datetime" header="Tarih" [style]="{'width':'10px'}"></Column>
        <Column field="level" header="Seviye"></Column>
        <Column field="message" header="Mesaj"></Column>
      </DataTable>
    </div>
  </div> -->

  <div class=" d-flex w-100 h-100 p-3 flex-column">
     
     <div class="container-fluid">
       <div class="row">

         <div class="col-md-3">

           <div class="btn-group mb-3 btn-group-sm" role="group">
             <button type="button" class="btn btn-outline-success">Göreve Başla</button>
             <button type="button" class="btn btn-outline-success">Görevi Duraklat</button>
             <button type="button" class="btn btn-outline-success">Görevi Tamamla</button>
             <button type="button" class="btn btn-outline-success">Otonom İniş</button>
             <button type="button" class="btn btn-outline-success">Eve Dönüş</button>
           </div>

           <div class="card text-bg-dark mb-3">
             <div class="card-header text-green">
               BAĞLANTI BİLGİLERİ
             </div>
             <div class="card-body">
               <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Yer istasyonu</p>
                 <p class="card-text text-green">Bağlandı</p>
               </div>

                <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Hakem Sunucu</p>
                 <p class="card-text text-danger">Bağlı değil</p>
               </div>

                <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">IHA Bağlantı</p>
                 <p class="card-text text-secondary">Bilgi yok</p>
               </div>

                <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Yarışma Süresi</p>
                 <p class="card-text text-secondary">Bilgi yok</p>
               </div>

             </div>
           </div>

           <div class="card text-bg-dark mb-3">
             <div class="card-header text-green">
               SUNUCU BİLGİLERİ
             </div>
             <div class="card-body">

               <div class="mb-2 row align-items-center">
                 <label for="takim_no" class="col-sm-4 col-form-label">Takım No.</label>
                 <div class="col-sm-8">
                   <input type="text" class="form-control form-control-sm" id="takim_no">
                 </div>
               </div>

               <div class="mb-2 row align-items-center">
                 <label for="hakem_sunucu" class="col-sm-4 col-form-label">Hakem Sunucu</label>
                 <div class="col-sm-5">
                   <input type="text" class="form-control form-control-sm" id="hakem_sunucu">
                 </div>

                 <div class="col-sm-3">
                   <input type="text" class="form-control form-control-sm" id="hakem_sunucu_port">
                 </div>
               </div>

               <div class="mb-2 row align-items-center">
                 <label for="iha_adres" class="col-sm-4 col-form-label">IHA Adres</label>
                 <div class="col-sm-5">
                   <input type="text" class="form-control form-control-sm" id="iha_adres">
                 </div>

                 <div class="col-sm-3">
                   <input type="text" class="form-control form-control-sm" id="iha_adres_port">
                 </div>
               </div>

               <div class="mb-2 row align-items-center">
                 <label for="username" class="col-sm-4 col-form-label">Kullanıcı Adı</label>
                 <div class="col-sm-8">
                   <input type="text" class="form-control form-control-sm" id="username">
                 </div>
               </div>

               <div class="mb-2 row align-items-center">
                 <label for="password" class="col-sm-4 col-form-label">Şifre</label>
                 <div class="col-sm-8">
                   <input type="text" class="form-control form-control-sm" id="password">
                 </div>
               </div>

               <div class="d-grid gap-2 mt-3">
                  <a href="#" class="btn btn-success">Kaydet</a>
               </div>
              
             </div>
           </div>

           <div class="card text-bg-dark mb-3">
             <div class="card-header text-green">
               GÖREV BİLGİLERİ
             </div>
             <div class="card-body">
               <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Yarışma Süresi</p>
                 <p class="card-text">00:00</p>
               </div>

                <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Son Kilitlenme</p>
                 <p class="card-text">156879</p>
               </div>

                <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Kilitlenilen İHA Sayısı</p>
                 <p class="card-text">5</p>
               </div>

                <div class="d-flex justify-content-between flex-row">
                 <p class="card-text">Kamikaze Görevi</p>
                 <p class="card-text text-green">Yapıldı</p>
               </div>

             </div>
           </div>

         </div>

         <div class="col-md-9">
           <div class="row">
             <div class="col-md-6">
               <img class="img-fluid" src="https://via.placeholder.com/1280x960" alt="kamera">
             </div>

             <div class="col-md-6">
               <img class="img-fluid" src="https://via.placeholder.com/1280x960" alt="harita">
             </div>

             <div class="col-md-12 mt-4">
               <img class="img-fluid" src="https://via.placeholder.com/1500x300" alt="kadran">
             </div>

             <div class="col-md-12">
              <DataTable :value="logList" :scrollable="true" scrollHeight="380px" tableStyle="{'width':'auto'}" class="table table-dark table-dark-hover mt-3">
                <Column field="datetime" header="Tarih" [style]="{'width':'10px'}"></Column>
                <Column field="level" header="Seviye"></Column>
                <Column field="message" header="Mesaj"></Column>
              </DataTable>
             <!-- <table class="table table-dark table-dark-hover mt-3">
               <thead>
                 <tr>
                   <th scope="col">#</th>
                   <th scope="col">First</th>
                   <th scope="col">Last</th>
                   <th scope="col">Handle</th>
                 </tr>
               </thead>
               <tbody>
                 <tr>
                   <th scope="row">1</th>
                   <td>Mark</td>
                   <td>Otto</td>
                   <td>@mdo</td>
                 </tr>
                 <tr>
                   <th scope="row">2</th>
                   <td>Jacob</td>
                   <td>Thornton</td>
                   <td>@fat</td>
                 </tr>
                 <tr>
                   <th scope="row">3</th>
                   <td colspan="2">Larry the Bird</td>
                   <td>@twitter</td>
                 </tr>
               </tbody>
             </table> -->
           </div>    

           </div>
         </div>

         


           
         </div><!-- row -->

       </div><!--container-fluid-->
     </div>
     
</template>

<script>

import sunucuBilgileriJSON from '../../sunucu_bilgileri.json'
import arayuzAssetVerileri from '@/assets/arayuz_assetleri.json'

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';

export default {
  name: 'App',
  components:{
    [DataTable.name]:DataTable,
    [Column.name]:Column,
    [Button.name]:Button,
  },
  data(){
    return {
      sunucuBilgileri:JSON.parse(JSON.stringify(sunucuBilgileriJSON)),

      yerIstasyonuWebsocket:null,
      websocketBaglantiTimeout:5000, // 5 sn

      yerIstasyonuBagli:false,
      hakemSunucuBagli:false,
      ihaDurum:'Bilgi yok',
      yarismaSuresi:'Bilgi yok', // Nasi yapilir ? Sunucudan da gelebilir.
      
      msg:'',
      response:'',
      logs:'',
      logSeviyeITOS:{
        0:'NOTSET',
        10:'DEBUG',
        20:'INFO',
        30:'WARNING',
        40:'ERROR',
        50:'CRITICAL',
      },
      logSeviyeSTOI:{
        NOTSET:0,
        DEBUG:10,
        INFO:20,
        WARNING:30,
        ERROR:40,
        CRITICAL:50,
      },
      logList:[
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
        {'datetime':'01/01/2032 16:23:05:159873','level':'INFO','message':'Test Mesajı'},
      ],

      canvasBoyutlari:{ // Canvas boyutları dinamik degisecek, buraya asagıda asıl değerler atanacak, bu değerler geçici
        'kamera-ibreler-canvas':{en:100,boy:100},
        'kalman-harita-canvas':{en:100,boy:100},
      },
      ibreBoyutlari:{
        en:200,
        boy:200,
      },
      arayuzAssetleri:{},
      ibreCizimSirasi:[ // Ibrelerin cizim sirasi. Birbirinin ustune cizmemesi icin
        'hiz_gosterge',
        'hiz_ibre',
        'irtifa_gosterge',
        'irtifa_ibre',
        'pitch_yaw_bg', // GEÇİCİ SONRA ÇIKAR DİNAMİK DOLDUR
        'yatis_ok',
        'pitch_yaw_gosterge',
        'pitch_yaw_imlec',
        'pusula_gosterge',
        'pusula_imlec',
      ],
      ibreKameraCanvasOran:{ // İbre kamera canvas'ının layout oranlanması
        ibre:{en:0.2,boy:0.3},
        kamera:{en:1,boy:0.8},
      },
    }
  },
  created(){
    this.websocketSetup();
  },
  mounted(){
    this.arayuzAssetYukle().then(() => this.gostergePaneliCiz());
    this.logTableAsagiScroll();
  },
  methods:{
    websocketSetup(){
      this.loglaraEkle(
        {
          datetime:this.logAnlikZaman(),
          level:this.logSeviyeSTOI.INFO,
          message:'Yer istasyonuna baglaniliyor...'
        }
      );
      this.yerIstasyonuWebsocket=new WebSocket(this.sunucuBilgileri.arayuz_ws);
      
      this.yerIstasyonuWebsocket.onopen=this.wsOnOpen;
      this.yerIstasyonuWebsocket.onclose=this.wsOnError;
      // this.yerIstasyonuWebsocket.onerror=this.wsOnError;
      this.yerIstasyonuWebsocket.onmessage=this.wsOnMessage;
    },
    veriGonder(){
      this.yerIstasyonuWebsocket.send(this.msg);
      this.msg='';
    },
    wsOnOpen(event){
      this.yerIstasyonuBagli=true;
      this.loglaraEkle(
        {
            datetime:this.logAnlikZaman(),
            level:this.logSeviyeSTOI.INFO,
            message:'Yer istasyonuna baglanildi.'
          }
        
      );
      this.$forceUpdate();
    },
    wsOnError(event){
      this.yerIstasyonuBagli=false;
      this.loglaraEkle(
        {
          datetime:this.logAnlikZaman(),
          level:this.logSeviyeSTOI.ERROR,
          message:'Yer istasyonu baglantisi beklenmedik bir sekilde kapandi, 5 saniye icinde  tekrar deneniyor.'
        }
      );
      this.$forceUpdate();
      new Promise(
        resolve => setTimeout(() => this.websocketSetup(),this.websocketBaglantiTimeout)
      );
    },
    wsOnMessage(data){
      data=data.data
      var jsonData=JSON.parse(data);
      var msgType=jsonData['type'];
      var msg=jsonData['data'];
      switch(msgType){
        case 'log': // Data olarak log mesajı string olarak gelir
          this.loglaraEkle(msg);
          this.$forceUpdate();
          break;
        case 'hakem_sunucu_bagli': // Data olarak hakem sunucu baglanti durumu boolean olarak gelir
          this.hakemSunucuBagli=msg;
          this.$forceUpdate();
        case 'kamera':
          document.getElementById('kamera').src=`data:image/png;base64,${msg}`;
      }
    },
    wsSendMessage(msg){
      if(this.yerIstasyonuWebsocket===null){
        this.loglaraEkle(
          {
            datetime:this.logAnlikZaman(),
            level:this.logSeviyeSTOI.ERROR,
            message:`Yer istasyonu baglantisi koptugundan mesaj gonderilemedi: ${msg}`
          }
        );
        this.$forceUpdate();
        return false;
      }
      this.yerIstasyonuWebsocket.send(JSON.stringify(msg));
      return true;
    },
    logAnlikZaman(){
      var dt = new Date();
      return `${dt.getHours()}:${dt.getMinutes()}:${dt.getSeconds()}.${dt.getMilliseconds()}`;
    },
    loglaraEkle(log){
      this.logs+=`${log}\n`;
      this.logList.push(log);
      // Burdan sonrası asagi autoscroll
      var textarea = this.$refs.logtextarea;
      if(textarea===undefined || textarea === null)
        return;
      textarea.scrollTop = textarea.scrollHeight;
      this.$forceUpdate();
      this.logTableAsagiScroll();
    },
    logTableAsagiScroll(){
      var dt= document.getElementsByClassName('ui-datatable-scrollable-body')[0];
      if(dt===undefined || dt===null) return
      dt.scrollTop = dt.scrollHeight - dt.clientHeight;
    },
    ykiSunucuBilgileriGuncelle(){
      var msg={type:'sunucu_bilgileri_guncelle',data:this.sunucuBilgileri};
      this.wsSendMessage(msg)
    },
    async arayuzAssetYukle(){
      const loadImage = asset => new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        // img.konum={
        //   x:asset.konum.x,
        //   y:asset.konum.y
        // }
        img.assetAdi=asset.assetAdi;
        img.src = require(`./assets/${asset.dosya}`);
      })

      var assetMap=[];
      for(var assetAdi in arayuzAssetVerileri){
        var assetVerisi=arayuzAssetVerileri[assetAdi];
        assetVerisi.assetAdi=assetAdi;
        assetMap.push(assetVerisi);
      }

      await Promise.all(assetMap.map(loadImage)).then(images => {
        for(var i in images){
          var image=images[i];
          this.arayuzAssetleri[image.assetAdi]=image;
        }
      });
    },
    gostergePaneliCiz(){
      // TODO: Buraya parametre olarak gelen telemetri verilerine göre açıları vs. hesaplayıp çizdir.
      this.gostergeCiz('hiz-gosterge','hiz_gosterge');
      this.ibreCiz('hiz-gosterge','hiz_ibre',0);

      this.gostergeCiz('irtifa-gosterge','irtifa_gosterge');
      this.ibreCiz('irtifa-gosterge','irtifa_ibre',135+0); // 0 noktası 135 derecede işaret ediliyor.

      // TODO: Bu göstergeyi incelemek lazım
      this.gostergeCiz('pitch-yaw-gosterge','pitch_yaw_bg'); // TODO: Burayı çizdirmek gerekicek
      this.gostergeCiz('pitch-yaw-gosterge','yatis_ok');
      this.gostergeCiz('pitch-yaw-gosterge','pitch_yaw_gosterge');
      this.gostergeCiz('pitch-yaw-gosterge','pitch_yaw_imlec');

      this.gostergeCiz('pusula-gosterge','pusula_gosterge');
      this.ibreCiz('pusula-gosterge','pusula_imlec',0);
    },
    gostergeCiz(canvasId, gostergeAdi){
      this.canvasaCiz(
        canvasId,
        this.arayuzAssetleri[gostergeAdi],
        0,
        0,
        this.ibreBoyutlari.en,
        this.ibreBoyutlari.boy,
        null
      )
    },
    ibreCiz(canvasId, ibreAdi, aci){
      this.canvasaCiz(
        canvasId,
        this.arayuzAssetleri[ibreAdi],
        0,
        0,
        this.ibreBoyutlari.en,
        this.ibreBoyutlari.boy,
        aci === 0 ? null : aci, // Açı 0 ise null değilse gelen değeri gönder
      )
    },
    dereceToRadyan(derece){
      return derece * (Math.PI/180);
    },
    canvasaCiz(canvasId,resim,x,y,en,boy,rotate){
      var canvas=document.getElementById(canvasId);
      var ctx=canvas.getContext('2d');
      if(rotate!==null){
        ctx.save();
        ctx.translate(en/2,boy/2);
        ctx.rotate(this.dereceToRadyan(rotate));
        ctx.drawImage(resim,-en/2,-boy/2,en,boy);
        ctx.restore()
      }
      else {
        ctx.drawImage(resim,x,y,en,boy);
      }
    },
    ibreleriCiz(){
      var ibreler=[]
      for(var i in this.arayuzAssetleri){
        var konum_x=this.arayuzAssetleri[i].konum.x;
        if(!ibreler.includes(konum_x))
          ibreler.push(konum_x);
      }
      
      for(var i in this.ibreCizimSirasi){
        var assetAdi=this.ibreCizimSirasi[i];
        var asset=this.arayuzAssetleri[assetAdi];
        var rotate=null;
        if(assetAdi=='irtifa_ibre'){
          rotate=this.dereceToRadyan(135);
        }
        else if(assetAdi=='hiz_ibre'){
          rotate=this.dereceToRadyan(0)
        }
        this.canvasaCiz(
          'kamera-ibreler-canvas',
          asset,
          (asset.konum.x*this.canvasBoyutlari['kamera-ibreler-canvas'].en)+this.ibreBoyutlari.padding,
          (asset.konum.y*this.canvasBoyutlari['kamera-ibreler-canvas'].boy)-this.ibreBoyutlari.boy+this.canvasBoyutlari['kamera-ibreler-canvas'].boy,
          this.ibreBoyutlari.en,
          this.ibreBoyutlari.boy,
          rotate
        );
      }
    },
    goreviBaslat(){
      var msg={type:'goreve_basla',data:null};
      this.wsSendMessage(msg);
    }
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
} */

.container {
  display:flex;
  flex-direction: column;
}

.bilgiler-kamera-kalman {
  display: flex;
  margin-left: 10px;
  margin-right: 10px;
}

.bilgiler {
  display: flex;
  flex-direction: column;
  margin-right: 10px;
}

.bilgiler > * {
  border: solid 1px;
}

.satir-1 {
  display: flex;
}

.sunucu-bilgileri {
  display:flex;
  flex-direction:column;
}

.bilgi-satir {
  display:flex;
  justify-content: space-between;
  align-items: baseline;
  max-height: 40px;
}

.kamera-ibreler-kalman {
  display:flex;
  flex-direction: column;
}

.kamera-kalman {
  display:flex;
}

.kamera-kalman > * {
  border: solid 1px black;
}

.ibreler {
  display:flex;
  justify-content: center;
  background-color: black;
  border: 5px solid gray;
  border-bottom-right-radius: 50px;
  border-bottom-left-radius: 50px;
}
.ibreler > * {
  margin-right: 10px;
}

.kalman-harita {
  /* background-color: green; */
  border: solid 1px black;
  width: 40%;
}

/* #kamera-ibreler-canvas {
  width: 33%;
} */

.hizli-komutlar-satir {
  display:flex;
  flex-direction: column;
}

.hizli-komutlar {
  display: flex;
  justify-content: center;
}

.yki-komut {
  display:flex;
  justify-content: center;
}

.log-satir {
  display:flex;
  flex-direction: row;
}

.log-kayitlari {
  display:flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 0.5%;
  margin: 0.5%;
  width: 100%;
}

#logtextarea {
  width:100%;
  min-height: 250%;
}

#logtable tr{
  font-size:13px;
  height : 30px;
}

body {
        font-family: Roboto Mono;
        background-color: #121212;
      }

      .text-green {
        color: #94bc2f !important;
      }


      .btn-outline-success {
        --bs-btn-color: #94bc2f;
        --bs-btn-border-color: #94bc2f;
        --bs-btn-hover-color: #fff;
        --bs-btn-hover-bg: #94bc2f;
        --bs-btn-hover-border-color: #94bc2f;
        --bs-btn-focus-shadow-rgb: 25,135,84;
        --bs-btn-active-color: #fff;
        --bs-btn-active-bg: #94bc2f;
        --bs-btn-active-border-color: #94bc2f;
        --bs-btn-active-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
        --bs-btn-disabled-color: #94bc2f;
        --bs-btn-disabled-bg: transparent;
        --bs-btn-disabled-border-color: #94bc2f;
        --bs-gradient: none;
      }

      .btn-success {
        --bs-btn-color: #fff;
        --bs-btn-bg: #94bc2f;
        --bs-btn-border-color: #94bc2f;
        --bs-btn-hover-color: #fff;
        --bs-btn-hover-bg: #648121;
        --bs-btn-hover-border-color: #648121;
        --bs-btn-focus-shadow-rgb: 60,153,110;
        --bs-btn-active-color: #fff;
        --bs-btn-active-bg: #648121;
        --bs-btn-active-border-color: #13653f;
        --bs-btn-active-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
        --bs-btn-disabled-color: #fff;
        --bs-btn-disabled-bg: #94bc2f;
        --bs-btn-disabled-border-color: #94bc2f;
      }

</style>
