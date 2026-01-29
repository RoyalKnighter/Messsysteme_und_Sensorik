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


block_size = 40  # Anzahl Punkte pro Block
y4 = []          # neue, zusammengefasste Werte
t4 = []          # dazugehörige Zeiten (z.B. Mittelwert des Blocks)

# Zusammenfassen in Blöcke
for i in range(0, y3.size, block_size):
    block = y3[i:i+block_size]
    t_block = t[i:i+block_size]
    
    # z.B. Mittelwert des Blocks
    y4.append(np.mean(block))
    t4.append(np.mean(t_block))

y4 = np.array(y4)
t4 = np.array(t4)


# --- Schritt 4: Plotten ---
plt.figure(figsize=(10, 5))

plt.plot(t, y1, label="CH2", color="blue")
plt.plot(t, 2*y2, label="CH3", color="pink")
#plt.plot(t, y3, label="Gefiltert", color="yellow")
#plt.plot(t4, y4, label="Gefiltert-2", color="green")

plt.xlabel("Zeit [s]")
plt.ylabel("Spannung [V]")
plt.title("Oszilloskop Signal")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

