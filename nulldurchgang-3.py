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
count_array = []
durchbruch_array = []

block_size = 100  # Anzahl Punkte pro Block

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

i = 1
while i < y4.size:
    #print("punkt: ", i, "t: ", t4[i], " y4: ", y4[i])
    if y4[i] == 0.0: #2
        durchbruch_array.append(i)
    elif y4[i-1] > 0.0 and y4[i] < 0.0: #3
        durchbruch_array.append(i)
    elif y4[i-1] < 0.0 and y4[i] > 0.0: #4
        durchbruch_array.append(i)
    i  += 1

durchbruch_array = np.array(durchbruch_array)

i = 1
while i < durchbruch_array.size:
    frequenz = 1/(2*(t4[durchbruch_array[i]]-t4[durchbruch_array[i-1]]))
    print(i, " frequenz: ", frequenz, " t4n: ", t4[durchbruch_array[i]], " t4n-1: ", t4[durchbruch_array[i-1]])
    if frequenz in frequenzen_arary:
        count_array[frequenzen_arary.index(frequenz)] += 1
    else:
        frequenzen_arary.append(frequenz)
        count_array.append(1)
    
    i += 1

print(y4.size)
print(durchbruch_array.size)
print(durchbruch_array)
print(frequenzen_arary)
print(count_array)

frequenzen_arary = np.array(frequenzen_arary)
count_array = np.array(count_array)

summe = 0

for i in range(0, frequenzen_arary.size):
    count_array[i] * frequenzen_arary[i]
    summe += count_array[i] * frequenzen_arary[i]

print("Frequenz: ", (summe/sum(count_array)))

plt.figure(figsize=(9,6))
plt.stem(frequenzen_arary, count_array)
#plt.xlim(300, 600)
#plt.ylim(0, 10)
plt.title('frequenz')
plt.grid(True)

plt.show()