import pandas as pd 
import matplotlib.pylab as plt 

temp=pd.read_csv("C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/temp_only.csv",parse_dates=["timestamp"]).set_index("timestamp")
curr=pd.read_csv("C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/current_only.csv",parse_dates=["timestamp"]).set_index("timestamp")


# Sıra bazlı merge
df=pd.DataFrame({
    "temp_c":temp["temp_c"].values,
    "current_a":curr["current_a"].values
})
df.index=range(len(df)) #basit index(0,1,2...N)


#rolling anomaly 
win=20

for col in ["temp_c","current_a"]:
    df[f"{col}_mean"]=df[col].rolling(win, min_periods=1).mean()
    df[f"{col}_std"]=df[col].rolling(win, min_periods=1).std(ddof=0)
    z=(df[col]-df[f"{col}_mean"])/(df[f"{col}_std"]+1e-6)
    df[f"{col}_anomaly"]=(z.abs()>2.5).astype(int)



print("Temp anomaly:",df["temp_c_anomaly"].sum())
print("Current anomaly:",df["current_a_anomaly"].sum())



#Dual axis 
fig,ax1=plt.subplots(figsize=(12,5))

ax1.plot(df.index, df["temp_c"], color="red", alpha=0.6, label="Temp (°C)")
ax1.plot(df.index, df["temp_c_mean"], color="darkred", label="Temp Mean")
ax1.scatter(df[df["temp_c_anomaly"]==1].index,
            df[df["temp_c_anomaly"]==1]["temp_c"],
            color="orange", label="Temp Anom", zorder=10)
ax1.set_ylabel("Temperature (°C)", color="red")
ax1.tick_params(axis="y", labelcolor="red")

# akım
ax2 = ax1.twinx()
ax2.plot(df.index, df["current_a"], color="blue", alpha=0.6, label="Current (A)")
ax2.plot(df.index, df["current_a_mean"], color="navy", label="Curr Mean")
ax2.scatter(df[df["current_a_anomaly"]==1].index,
            df[df["current_a_anomaly"]==1]["current_a"],
            color="cyan", label="Curr Anom", zorder=10)
ax2.set_ylabel("Current (A)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

plt.title("Temperature & Current with Anomalies")
fig.tight_layout()

# Legend birleştirme
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines1+lines2, labels1+labels2, loc="upper right")

plt.show()
