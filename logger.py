import os
from datetime import datetime
import logging
from threading import Thread,Lock

class Logger:
    def __init__(self,log_level:int=logging.INFO):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        self.filename=f'logs/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}_YKI.log'
        self.log_file_lock=Lock()
        
        self.log_levels={
            logging.NOTSET:'NOTSET',
            logging.DEBUG:'DEBUG',
            logging.INFO:'INFO',
            logging.WARNING:'WARNING',
            logging.ERROR:'ERROR',
            logging.CRITICAL:'CRITICAL',
        }
        self.log_level=log_level
        
        self.arayuz=None # Arayuz set edicek
    
    def set_arayuz(self,arayuz):
        self.arayuz=arayuz
    
    def log(self,*msg,log_level:int=logging.INFO, arayuze_gonder:bool=True,yazdir:bool=True):
        if log_level<self.log_level:
            return None
        
        current_datetime=datetime.now().strftime('%H:%M:%S.%f')
        msg=' '.join(str(m) for m in msg)
        log_data={
            'datetime':current_datetime,
            'level':log_level,
            'message':msg,
        }

        log_line=f"{log_data['datetime']} - {self.log_levels[log_data['level']]} - {log_data['message']}"
        with self.log_file_lock:
            with open(self.filename,'a') as f:
                f.write(log_line+'\n')
        if yazdir:
            print(log_line)
        
        if arayuze_gonder:
            if  self.arayuz is None:
                self.log('Arayuze gonderme basarisiz: Logger arayuzu None',log_level=logging.ERROR,arayuze_gonder=False)
            elif not self.arayuz.send('log',log_data):
                self.log('Arayuze gonderme basarisiz: Send metodu False dondu',log_level=logging.ERROR,arayuze_gonder=False)
        
        return log_data