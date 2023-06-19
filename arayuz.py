import asyncio
import websockets
from threading import Thread
import json
import time
import logging

from logger import Logger

class YerIstasyonuArayuz:
    def __init__(self,logger:Logger):
        self.websocket=None
        self.messages=[]

        self.logger:Logger=logger
        self.logger.set_arayuz(self)

        self.loop_cakisma_retry=3 # Loop cakismasinda retry sayisi, send metoduna bak
        self.loop=asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    @property
    def is_connected(self):
        return self.websocket is not None

    # Setup wrapper metodu.
    def setup(self):
        # loop=asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        self.loop.run_until_complete(
            self._setup()
        )

    # Mesajlari dinleyen metod
    async def ws_handler(self,websocket):
        self.websocket=websocket
        self.logger.log('Arayuz websocket baglantisi tamamlandi.',arayuze_gonder=False)
        while not websocket.closed:
            async for msg in websocket:
                self.messages.append(msg)

        self.logger.log('Arayuz websocket baglantisi koptu. Tekrar baglanma bekleniyor.',arayuze_gonder=False)
        self.websocket=None
    
    # Arayuzden gelen mesajlari ileten generator metod
    def arayuz_messages(self):
        while self.messages:
            yield self.messages.pop(0)

    # Mesaj gonderme metodu wrapper
    def send(self,type,message):
        if self.websocket is None:
            return False
        
        message=json.dumps({'type':type,'data':message})
        for i in range(self.loop_cakisma_retry):
            try:
                send_loop=asyncio.new_event_loop()
                send_loop.run_until_complete(
                    self._send(message)
                )
                return True
            except RuntimeError: # Bazen asyncio looplari cakisabiliyor, cakistiginda tekrar denesin
                self.logger.log(
                    f'Arayuze gonderirken loop cakismasi meydana geldi, tekrar deneniyor {i+1}/{self.loop_cakisma_retry}',
                    log_level=logging.ERROR,
                    arayuze_gonder=False
                )
                time.sleep(3)
        
        return False
    
    # Mesaj gonderme metodu. Direk kullanamazsın, wrapper'i cagir
    async def _send(self,message):
        await self.websocket.send(message)

    # Websocketin kurulumunu yapar.
    async def _setup(self):
        async with websockets.serve(self.ws_handler,'',6789):
            await asyncio.Future()
    
    def start(self):
        self.logger.log('Arayuz websocket baslatiliyor...',arayuze_gonder=False)
        Thread(target=self.setup).start()
        self.logger.log('Arayuz websocket baslatildi, baglanti bekleniyor...',arayuze_gonder=False)
        while self.websocket is None:
            continue # Busy waiting. Bağlantı gelene kadar bekler.