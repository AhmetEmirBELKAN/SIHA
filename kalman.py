import numpy as np
from pykalman import KalmanFilter
import random
import time

class IHAKalman:
    def __init__(self,baslangic_lat:float,baslangic_lon:float):
        self.koordinatlar:np.array = np.array([(baslangic_lat,baslangic_lon)])
        # print(self.koordinatlar)

    def tahmin(self):
        # Gelen veri azsa tahmine başlamasın. Kaldırılabilir.
        # if len(self.koordinatlar)<8:
        #     return None
        
        # print(self.koordinatlar)
        # print(self.koordinatlar[0])
        initial_state_mean=[
            self.koordinatlar[0,0],
            0,
            self.koordinatlar[0,1],
            0
        ]

        transition_matrix = [
            [1,1,0,0],
            [0,1,0,0],
            [0,0,1,1],
            [0,0,0,1],
        ]

        observation_matrix = [
            [1,0,0,0],
            [0,0,1,0]
        ]

        kalman_filter=KalmanFilter(
            transition_matrices=transition_matrix,
            observation_matrices=observation_matrix,
            initial_state_mean=initial_state_mean,
        )

        kalman_filter=kalman_filter.em(self.koordinatlar,n_iter=8)
        (smoothed_state_means, smoothed_state_covariances) = kalman_filter.smooth(self.koordinatlar)

        new_lat=smoothed_state_means[:, 0]
        new_lon=smoothed_state_means[:, 2]

        return {
            'lat':list(self.koordinatlar[:,0])+[new_lat[-1]],
            'lon':list(self.koordinatlar[:,1])+[new_lon[-1]],
        }
    
    def koordinat_ekle(self,lat:float,lon:float):
        self.koordinatlar = np.concatenate((self.koordinatlar,np.array([(lat,lon)])))
        if len(self.koordinatlar)>8:
            self.koordinatlar=self.koordinatlar[1:]


if __name__=='__main__':
    print(time.time())
    kf=IHAKalman(random.uniform(0.0,50.0),random.uniform(0.0,100.0))
    for _ in range(100):
        kf.koordinat_ekle(random.uniform(0.0,50.0),random.uniform(0.0,100.0))
        # kf.tahmin()
        print(kf.tahmin())
    # kf=IHAKalman(41.25770002,36.55490357)
    # kf.koordinat_ekle(41.68465,36.55490367)
    # kf.koordinat_ekle(42.58972,36.5549035)
    # kf.koordinat_ekle(41.96248,36.5549035)
    # kf.koordinat_ekle(40.123578,36.55490366)
    # kf.koordinat_ekle(41.25770017,36.5549036) 
    kf.tahmin()
    print(time.time())