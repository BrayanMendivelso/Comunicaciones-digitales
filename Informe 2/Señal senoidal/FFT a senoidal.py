import numpy as np
import matplotlib.pyplot as plt
archivo_csv = r'D:\Universidad\Semestre 6\Comunicaciones digitales\Informe 2\Señal senoidal\con offset\FFT1offset.csv'
data = np.loadtxt(archivo_csv, delimiter=",", skiprows=12, usecols=(3, 4))
frecuencias = data[:, 0]
dB = data[:, 1]
idx_max = np.argmax(dB)
f_dominante = frecuencias[idx_max]*99
dB_max = dB[idx_max]
amplitud = 10**(dB_max / 20)*1.4
fs = 50000  
duracion = 0.001  
t = np.linspace(0, duracion, int(fs*duracion), endpoint=False)
senal = amplitud * np.cos(2 * np.pi * f_dominante * t)+1
plt.plot(t * 1000, senal)  
plt.xlabel("Tiempo [ms]")
plt.ylabel("Amplitud")
plt.title(f"Señal senoidal reconstruida")
plt.grid(True)
plt.show()


