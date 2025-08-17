
import pandas as pd
import matplotlib.pylab as plt

temp=pd.read_csv("C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/temp_only.csv",parse_dates=["timestamp"])
curr=df=pd.read_csv("C:/Users/sinan/Desktop/python_proje/pandas_numpy/sensör/current_only.csv",parse_dates=["timestamp"])


temp["seq"]=range(len(temp))
curr["seq"]=range(len(curr))

#kontrol
# print("TEMP CSV kolonları:", temp.columns)
# print(temp.head(), "\n")
# print("CURR CSV kolonları:", curr.columns)
# print(curr.head())

#merge
df = temp[["seq","temp_c"]].merge(curr[["seq","current_a"]], on="seq", how="inner")
print(df.head(), df.shape)




#
fig, ax1 = plt.subplots(figsize=(12,5))

# temp
ax1.plot(df.index, df["temp_c"], color="red", label="Temp (°C)")
ax1.set_ylabel("Temperature (°C)", color="red")
ax1.tick_params(axis="y", labelcolor="red")

# ikinci eksen
ax2 = ax1.twinx()
ax2.plot(df.index, df["current_a"], color="blue", label="Current (A)")
ax2.set_ylabel("Current (A)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")
plt.title("Temprature and Current(dual)")
plt.tight_layout()
plt.show()