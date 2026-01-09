import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

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

y = y1-2*y2

# --- Sampling / Abtastrate ---
dt = t[1] - t[0]
fs = 1.0 / dt
N = len(y)
print(f"Abtastrate fs = {fs:.0f} Hz, Samples N = {N}, Frequenzauflösung df = {fs/N:.3f} Hz")

# --- 1) Preprocessing: DC entfernen und Fenster anwenden ---
y = y - np.mean(y)                 # DC entfernen
window = np.hanning(N)             # Hann-Fenster
y_win = y * window

# --- 2) FFT ---
Y = np.fft.rfft(y_win)             # rfft -> nur positive Frequenzen
freq = np.fft.rfftfreq(N, d=dt)    # korrespondierende Frequenzen

# --- 3) Normierte Amplitude (konventionell: 2/N * |Y|, angepasst durch Fensterenergie) ---
# Normierung durch die Summe des Fensters um Amplitudenverfälschung zu reduzieren
amplitude = (2.0 * np.abs(Y)) / np.sum(window)

# --- 4) Schmale Suche um erwartete 460 Hz (z.B. 100..1000 Hz) ---
f_min, f_max = 0.0, 600.0  # anpassen falls nötig
mask = (freq >= f_min) & (freq <= f_max)
freq_band = freq[mask]
amp_band = amplitude[mask]

# --- 5) Grobe Peak-Suche (max im Band) ---
idx_rel = np.argmax(amp_band)           # index innerhalb des zugeschnittenen Bandes
idx = np.where(mask)[0][0] + idx_rel    # index innerhalb des kompletten freq-Arrays

# --- 6) Parabolische Interpolation (sub-bin Genauigkeit) ---
# Verwende drei Punkte: (k-1, k, k+1) wenn möglich
k = idx
if 1 <= k < len(amplitude) - 1:
    # log-amplitude parabolische Interpolation (robuster bei großen Dynamiken)
    alpha = np.log(amplitude[k-1])
    beta  = np.log(amplitude[k])
    gamma = np.log(amplitude[k+1])

    p = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma)  # Verschiebung in Bins
    peak_freq = freq[k] + p * (freq[1] - freq[0])         # feiner geschätzte Frequenz
    peak_amp = np.exp(beta - 0.25*(alpha - gamma)*p)      # interpolierte Amplitude (optional)
else:
    peak_freq = freq[k]
    peak_amp = amplitude[k]

print(f"Gefundene dominante Frequenz (grob): {freq[k]:.2f} Hz")
print(f"Fein geschätzte Frequenz (parabolisch): {peak_freq:.4f} Hz")
print(f"Amplitude bei Peak (approx): {peak_amp:.6e}")

# --- 7) Plot: gesamtes Spektrum (log oder linear) + Zoom um Peak ---
plt.figure(figsize=(10,5))
plt.plot(freq, amplitude, label="FFT Amplitude")
plt.xscale("linear")
plt.ylim(bottom=0)
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude [relativ]")
plt.title("Frequenzspektrum (rFFT, Hann, DC entfernt)")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Marker für gefundenen Peak
plt.plot(peak_freq, peak_amp, 'ro', label=f"Peak {peak_freq:.2f} Hz")
plt.legend()
plt.show()

# Zoom-Plot um den erwarteten Bereich (besser sichtbar)
zoom_margin = 200.0  # Hz um den Peak herum zum Anzeigen
plt.figure(figsize=(10,4))
plt.plot(freq_band, amp_band)
plt.axvline(peak_freq, color='r', linestyle='--', label=f"Peak {peak_freq:.2f} Hz")
plt.xlim(max(0, peak_freq-zoom_margin), peak_freq+zoom_margin)
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title("Zoom um den gefundenen Peak")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,4))
plt.plot(freq_band, amp_band)
plt.axvline(50.0, color='r', linestyle='--', label=f"{50.0:.2f} Hz")
plt.xlim(max(0, 50.0-zoom_margin), 50.0+zoom_margin)
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude")
plt.title("Zoom um den gefundenen Peak")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
