# Comunicaciones Digitales UMNG / jose.rugeles@Unimilitar.edu.co
# Programa 1: Lectura ADC -> Voltios 

import machine
import utime

ADC_PIN = 26      # GP26 -> ADC0 (cambia a 27 o 28 si usas ADC1/ADC2)
VREF    = 3.300   # mide tu 3V3 real y ajústalo aquí para mejor exactitud
PERIOD  = 0.02    # segundos entre lecturas (0.05–0.5 )

adc = machine.ADC(ADC_PIN)

# El conversor analógico–digital (ADC) de los microcontroladores RP2040 ( Pico W) ó RP2350 ( Pico 2W) poseen
# una resolución de 12 bits, lo que significa que puede entregar valores enteros entre 0 y 4095
#(es decir, 212 − 1 niveles de cuantización). Sin embargo, la función read_u16() de MicroPython devuelve siempre
# un valor entero de 16 bits en el rango 0 a 65535. Para lograr esto, el valor de 12 bits obtenido
# del ADC es alineado hacia la izquierda dentro de los 16 bits, rellenando con cuatro ceros los
# bits menos significativos

while True:
    raw16  = adc.read_u16()      # 0..65535 (12 bits alineado a la izq.)
    code12 = raw16 >> 4          # 0..4095 (12 bits reales)
    volts  = (code12 * VREF) / 4095.0
    print(f"{volts:.4f}")        # <-- SOLO un número por línea
    utime.sleep(PERIOD)
