# HAm Sıcaklık Üretici

import numpy as np
import pandas as pd
from datetime import datetime,timedelta


N=1000 #örnekler
rate_HZ=10 # Hz
base_temp=24.0 # sicaklik
noise_std=0.15 # gürültü
seed=42 # tekrar üretebilirlik


# numpy ile Veri üretme 

rng=np.random.default_rng(seed) #RNG kurulumu 
t= np.arange(N) / rate_HZ  # saniye cinsinden zaman vektörü 
drift=0.02*(t / 60.0) # dakikaya göre çok küçük drift
temp=base_temp + drift+rng.normal(0,noise_std,N) #Temel +gürültü

# pandas DataFrame + timestap

start_ts=datetime.now() # başlangıç zamanı 
index=pd.date_range(start=start_ts, periods=N, freq=pd.Timedelta(seconds=1/rate_HZ)) #zaman indexi
df=pd.DataFrame({"temp_c":temp},index=index)
df.index.name="timestamp"


#Rolling öznitelikleri 

win=max(3, int(2*rate_HZ))
df["temp_roll_mean"]=df["temp_c"].rolling(win, min_periods=1).mean()
df["temp_roll_std"]=df["temp_c"].rolling(win, min_periods=1).std(ddof=0)





#çıktı 
print(df.head(10))
print("\nDescribe (temp_c):")
print(df["temp_c"].describe())



#CSV olarak save
out_csv="C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/temp_only.csv"
df.to_csv(out_csv,index=True)
print(f"\n[OK] CSV kaydedildi: {out_csv}")




# csv'yi okut

df=pd.read_csv(out_csv,parse_dates=["timestamp"])
df=df.set_index("timestamp")

# Rolling mean/std
win=20
df["m"]=df["temp_c"].rolling(win,min_periods=1).mean()
df["sd"]=df["temp_c"].rolling(win,min_periods=1).std(ddof=0)



# Z hesabi
eps= 1e-6 #sifira bölmeyi engelleme
df["z"]=(df["temp_c"]-df["m"]) /(df["sd"]+eps) 


#anomaly sütünü
df["anomaly"]=(df["z"].abs()>3).astype(int)


print(df.head(10))
print("Total Anomaly:",df["anomaly"].sum())



