import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv("C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/temp_only.csv",parse_dates=["timestamp"]).set_index("timestamp")


#Roling ve anomaly sütunlari
win=20 
df["m"]=df["temp_c"].rolling(win,min_periods=1).mean()
df["sd"]=df["temp_c"].rolling(win,min_periods=1).std(ddof=0)
eps=1e-6
df["z"]=(df["temp_c"]-df["m"]) / (df["sd"]+eps)
df["anomaly"]=(df["z"].abs()>3).astype(int)




#Grafikler
plt.figure(figsize=(12,15))
plt.plot(df.index, df["temp_c"], label="Temp (°C)", color="blue")
plt.plot(df.index, df["m"], label="Rolling Mean", color="orange")



#Anomaly
anoms=df[df["anomaly"]==1]
plt.scatter(anoms.index, anoms["temp_c"], color="red", label="Anomaly", zorder=5)


plt.title("Temperature with Anomalies")
plt.xlabel("Time")
plt.ylabel("°C")
plt.legend()
plt.tight_layout()
plt.show()