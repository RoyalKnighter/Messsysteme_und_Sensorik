import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Pfad zur CSV-Datei ---
file_path = "Messung-5.CSV"

with open(file_path) as f:
    for i, line in enumerate(f):
        if line.strip().startswith("TIME"):
            data_start = i
            break

df = pd.read_csv(file_path, skiprows=data_start)

print(df.head())

y1 = df["CH2"].values
y2 = df["CH3"].values
t = df["TIME"].values

y3 = y1-2*y2

# --- Autokorrelation ---
y3 = y3 - np.mean(y3)

autocorr = np.correlate(y3, y3, mode="full")
autocorr = autocorr[autocorr.size // 2:]

dt = t[1] - t[0]
lags = np.arange(len(autocorr)) * dt

f_min = 100      # Hz
f_max = 2000     # Hz

lag_min = int(1 / f_max / dt)
lag_max = int(1 / f_min / dt)

search_region = autocorr[lag_min:lag_max]
peak_index = np.argmax(search_region) + lag_min

T = lags[peak_index]
f = 1 / T

print(f"Periodendauer T = {T:.6e} s")
print(f"Frequenz f = {f:.2f} Hz")

plt.figure(figsize=(8,4))
plt.plot(lags, autocorr)
plt.axvline(T, color="r", linestyle="--", label=f"{f:.1f} Hz")
plt.xlim(0, 0.01)
plt.grid()
plt.legend()
plt.show()
