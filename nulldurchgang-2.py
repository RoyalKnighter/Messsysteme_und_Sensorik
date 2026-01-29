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

block_size_array = []
frequenzen_arary = []

block_size = 1  # Anzahl Punkte pro Block




while block_size < 3700:
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

    #print()
    #print(y3.size)
    #print()

    null = 0
    durchbruch1 = 0
    durchbruch2 = 0

    i = 1
    while i < y4.size:
        #print("punkt: ", i, "t: ", t4[i], " y4: ", y4[i])
        if y4[i] == 0.0: #2
            null = null + 1
            #print(null, " y4: ", y4[i])
            #print(null, " t: ", t[i])
        elif y4[i-1] > 0.0 and y4[i] < 0.0: #3
            durchbruch1 = durchbruch1 + 1
            #print(durchbruch1, " y4: ", y4[i])
            #print(durchbruch1, " t: ", t[i])
        elif y4[i-1] < 0.0 and y4[i] > 0.0: #4
            durchbruch2 = durchbruch2 + 1
            #print(durchbruch2, " y4: ", y4[i-1], " ", y4[i])
            #print(durchbruch2, " t: ", t[i])

        i  += 1


    #print()
    #print(null)
    #print(durchbruch1)
    #print(durchbruch2)
    #print()
    #print()

    durchbruch = null+durchbruch1+durchbruch2
    deltaT = t[t.size-1]-t[0]

    f = durchbruch/(2*deltaT)
    #print("durchbruch: ", durchbruch)
    #print("deltaT: ", deltaT)
    print("block_size: ", block_size, "durchbruch: ", durchbruch, "deltaT: ", deltaT, " frequenz: ", f)

    block_size_array.append(block_size)
    frequenzen_arary.append(f)
    block_size += 20


block_size_array = np.array(block_size_array)
frequenzen_arary = np.array(frequenzen_arary)


plt.figure(figsize=(9,6))
plt.stem(block_size_array, frequenzen_arary)
plt.xlim(0, 3700)
plt.ylim(200, 500)
plt.title('frequenz')
plt.grid(True)

plt.show()