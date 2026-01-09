import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Pfad zur CSV-Datei ---
file_path1 = "Messung-4-Signal.CSV"
file_path2 = "Messung-4-Störsignal.CSV"

with open(file_path1) as f:
    for i, line in enumerate(f):
        if line.strip().startswith("TIME"):
            data_start = i
            break

with open(file_path2) as f:
    for i, line in enumerate(f):
        if line.strip().startswith("TIME"):
            data_start = i
            break

df1 = pd.read_csv(file_path1, skiprows=data_start)
df2 = pd.read_csv(file_path2, skiprows=data_start)

print(df1.head())
print(df2.head())

y1 = df1["CH2"].values
y2 = df2["CH3"].values
t = df1["TIME"].values

y3 = y1-2*y2

# --- Schritt 4: Plotten ---
plt.figure(figsize=(10, 5))

plt.plot(t, y1, label="CH2", color="blue")
plt.plot(t, 2*y2, label="CH3", color="pink")
plt.plot(t, y3, label="Gefiltert", color="yellow")

plt.xlabel("Zeit [s]")
plt.ylabel("Spannung [V]")
plt.title("Oszilloskop Signal")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

