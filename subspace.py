import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig

# --- Pfad zur CSV-Datei ---
file_path = "Messung-5.CSV"

# CSV einlesen, ab Zeile mit "TIME"
with open(file_path) as f:
    for i, line in enumerate(f):
        if line.strip().startswith("TIME"):
            data_start = i
            break

df = pd.read_csv(file_path, skiprows=data_start)
print(df.head())

# Signal vorbereiten
y1 = df["CH2"].values
y2 = df["CH3"].values
t = df["TIME"].values
y3 = y1 - 2*y2



block_size = 1  # Anzahl Punkte pro Block
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

y5 = y3 - np.mean(y3)




# --- MUSIC-Frequenzanalyse ---
def music_frequency_estimation(signal, fs, n_sources=1, M=50):
    """
    signal: 1D numpy array
    fs: Abtastrate in Hz
    n_sources: Anzahl der zu schätzenden Sinus-Komponenten
    M: Dimension der Autokorrelationsmatrix (Fenstergröße)
    """
    N = len(signal)
    # Autokorrelationsmatrix R schätzen
    X = np.array([signal[i:i+M] for i in range(N-M)]).T
    R = np.dot(X, X.conj().T) / (N - M)
    
    # Eigenwerte und Eigenvektoren
    eigvals, eigvecs = eig(R)
    idx = eigvals.argsort()[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    
    # Noise-Subspace
    E_n = eigvecs[:, n_sources:]
    
    # Frequenzvektor
    freqs = np.linspace(0, fs/2, 2000)
    P = np.zeros_like(freqs)
    
    for i, f in enumerate(freqs):
        a = np.exp(-1j*2*np.pi*f*np.arange(M)/fs)
        P[i] = 1 / np.abs(a.conj().T @ E_n @ E_n.conj().T @ a)
    
    return freqs, 10*np.log10(P.real)

# Sampling
dt = t[1] - t[0]
fs = 1/dt

# Frequenzanalyse, größere M für 440 Hz
freqs, P_music = music_frequency_estimation(y5, fs, n_sources=1, M=50)

# Plot nur bis 2000 Hz
plt.figure(figsize=(10,5))
plt.plot(freqs, P_music)
plt.title("MUSIC-Spektrum von y3")
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Leistung [dB]")
plt.xlim(0, 2000)   # Zoom auf 0-2 kHz
plt.grid(True)
plt.show()
