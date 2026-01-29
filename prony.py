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

# Abtastzeit
T = np.mean(np.diff(t))
fs = 1 / T

# Modellordnung (2 Pole = 1 Sinus)
M = 2

# Lineares Gleichungssystem aufstellen
N = len(y3)
Y = np.zeros((N - M, M))
for i in range(M):
    Y[:, i] = y3[M - i - 1:N - i - 1]

b = -y3[M:N]

# Prony-Koeffizienten
a = np.linalg.lstsq(Y, b, rcond=None)[0]
a = np.concatenate(([1], a))

# Polstellen berechnen
poles = np.roots(a)

# Frequenzen und Dämpfung
freqs = np.angle(poles) / (2 * np.pi * T)
damping = np.log(np.abs(poles)) / T

# Nur positive Frequenzen betrachten
freqs = freqs[freqs > 0]
damping = damping[:len(freqs)]

print("Gefundene Frequenzen (Hz):")
print(freqs)

# ----------------------------------
# Vergleich: FFT
# ----------------------------------
Y_fft = np.fft.fft(y3)
freq_fft = np.fft.fftfreq(len(y3), T)

plt.figure(figsize=(10, 5))
plt.plot(freq_fft[:len(freq_fft)//2],
         np.abs(Y_fft[:len(Y_fft)//2]))
plt.axvline(freqs[0], color='r', linestyle='--',
            label=f"Prony: {freqs[0]:.2f} Hz")
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.show()