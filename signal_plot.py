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

