# Akım Üretici

import numpy as np
import pandas as pd
from datetime import datetime


#Parameters 
n=1000
rate_hz=10
seed=42
rng=np.random.default_rng(seed)



#Current Data
base_curr=1.2
noise_curr=0.05
curr=base_curr+rng.normal(0,noise_curr,n)



#Timestap and Dataframe
start_ts=datetime.now()
index=pd.date_range(start=start_ts,periods=n,freq=pd.Timedelta(seconds=1/rate_hz))
df=pd.DataFrame({"current_a":curr},index=index)
df.index.name="timestamp"



#Rolling 
win=max(3,int(2*rate_hz))
df["current_roll_mean"]=df["current_a"].rolling(win, min_periods=1).mean()
df["current_roll_std"]=df["current_a"].rolling(win,min_periods=1).std(ddof=0)

#çıktı 
print(df.head(10))
print("\nDescribe (current_a):")
print(df["current_a"].describe())


#csv olarak kaydet

out_csv="C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/current_only.csv"
df.to_csv(out_csv,index=True)




