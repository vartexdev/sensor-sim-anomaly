import pandas as pd
import numpy as np
import matplotlib.pylab as plt

df=pd.read_csv("C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/current_only.csv",parse_dates=["timestamp"]).set_index("timestamp")

win=20
df["m"]=df["current_a"].rolling(win, min_periods=1).mean()
df["sd"]=df["current_a"].rolling(win, min_periods=1).std(ddof=0)
eps=1e-6
df["z"]=(df["current_a"]-df["m"])/(df["sd"]+eps)
df["anomaly"]=(df["z"].abs()>2.6).astype(int)

print("Total Anomaly:", int(df["anomaly"].sum())) 

plt.figure(figsize=(12,5))
plt.plot(df.index, df["current_a"], label= "Current (A)",color="yellow")
plt.plot(df.index, df["m"],label="Rolling Mean", color="black")



#anomaly
anoms=df[df["anomaly"]==1]
plt.scatter(anoms.index, anoms["current_a"], color="red", label="Anomaly", zorder=5)



plt.title("Current with Anomalies")
plt.xlabel("Time")
plt.ylabel("A")
plt.legend() # renkerlin anlamlarını verir 
plt.tight_layout() 
plt.show()