import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import time

Fs = 44100
Ts = 1 / Fs
minF0Frequency = 80
maxF0Frequency = 300
minF0Period = 1 / minF0Frequency
maxF0Period = 1 / maxF0Frequency
Nbegin = round(maxF0Period / Ts) 
Nend = round(minF0Period / Ts)

if 1:
    print('Gravação inicializada. Diga uma vogal a, e, i, o ou u')
    y = sd.rec(int(2*Fs), samplerate=Fs, channels=1)[:, 0]
    sd.wait()
    print('Gravação finalizada')
else:
    y = np.cos(2 * np.pi * 300 * np.arange(0, 2 * Fs) * Ts)

plt.subplot(211)
plt.plot(Ts * np.arange(len(y)), y)
plt.xlabel('tempo (s)')
plt.ylabel('Sinal y(t)')

lags = np.arange(-Nend, Nend+1)
lags, R, _, _ = plt.xcorr(y, y, usevlines=True, maxlags=Nend, normed=True, lw=2)

plt.subplot(212)
plt.plot(lags * Ts, R)
plt.xlabel('lag (s)')
plt.ylabel('Autocorrelação de y(t)')

firstIndex = np.where(lags == Nbegin)[0][0]
Rpartial = R[firstIndex:]

Rmax, relative_index_max = max(Rpartial), np.argmax(Rpartial)
index_max = firstIndex + relative_index_max
lag_max = lags[index_max]

plt.plot(lag_max * Ts, Rmax, 'xr', linewidth=2)

F0 = 1 / (lag_max * Ts)
print(f'Rmax = {Rmax} lag_max = {lag_max} T = {lag_max * Ts} (s) Freq. = {F0} Hz')
t = np.arange(0, 2, Ts)

for i in range(3, 0, -1):
    print(f'Sinal com autocorrelação em {i}')
    time.sleep(1)

sd.play(np.cos(2 * np.pi * 3 * F0 * t), Fs)

plt.show()
