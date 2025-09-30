from machine import ADC, Pin
import utime, math

adc = ADC(26)
fs = 2000       # Frecuencia de muestreo [Hz]
N = 512         # Número de muestras
dt_us = int(1_000_000 / fs)

# Lista de frecuencias de interés para Goertzel
frequencies = [50, 200, 400]  # Hz

# Guardar resultados de FFT por frecuencia
fft_results = {f: 0.0 for f in frequencies}

# Jitter
intervals = []

# Archivo para la señal en tiempo real
with open("time3.csv", "w") as f_time:
    f_time.write("tiempo_s,voltaje_v\n")
    t_prev = utime.ticks_us()
    for i in range(N):
        # Tomar muestra
        sample = adc.read_u16()
        t_curr = utime.ticks_us()
        elapsed_us = utime.ticks_diff(t_curr, t_prev)
        intervals.append(elapsed_us)
        t_prev = t_curr

        # Convertir a voltaje
        volt = sample * 3.3 / 65535
        f_time.write(f"{i/fs:.6f},{volt:.5f}\n")

        # Procesar Goertzel en línea
        for freq in frequencies:
            # Recálculo simple Goertzel por muestra
            # Mantener variables internas por frecuencia
            if i == 0:
                fft_results[freq] = {'s_prev':0.0,'s_prev2':0.0}
            k = int(0.5 + N * freq / fs)
            omega = 2.0 * math.pi * k / N
            coeff = 2.0 * math.cos(omega)
            s = volt + coeff * fft_results[freq]['s_prev'] - fft_results[freq]['s_prev2']
            fft_results[freq]['s_prev2'] = fft_results[freq]['s_prev']
            fft_results[freq]['s_prev'] = s

# ==========================
# Calcular magnitudes finales de Goertzel
# ==========================
with open("fft3.csv", "w") as f_fft:
    f_fft.write("frecuencia_hz,magnitud_v\n")
    for freq in frequencies:
        s_prev = fft_results[freq]['s_prev']
        s_prev2 = fft_results[freq]['s_prev2']
        k = int(0.5 + N * freq / fs)
        omega = 2.0 * math.pi * k / N
        coeff = 2.0 * math.cos(omega)
        magnitude = math.sqrt(s_prev2**2 + s_prev**2 - coeff * s_prev * s_prev2) * 2 / N
        f_fft.write(f"{freq},{magnitude:.5f}\n")
        print(f"Frecuencia {freq} Hz -> Magnitud {magnitude:.5f} V")

# ==========================
# Calcular jitter
# ==========================
jitter_mean = sum(intervals)/len(intervals) - 1e6/fs
jitter_rms = (sum([(x - 1e6/fs)**2 for x in intervals])/len(intervals))**0.5

with open("jitter.csv", "w") as f_j:
    f_j.write("jitter_mean_us,jitter_rms_us\n")
    f_j.write(f"{jitter_mean:.3f},{jitter_rms:.3f}\n")

print(f"Jitter medio = {jitter_mean:.2f} us, RMS = {jitter_rms:.2f} us")
