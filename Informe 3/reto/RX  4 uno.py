import machine
import utime
from machine import Pin, UART

# LED en GP15
led = Pin(15, Pin.OUT)

# UART
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

# Contador de recepciones
contador = 0

while True:
    if uart.any():
        dato = uart.read(1)
        if dato == b"A":
            contador += 1
            print(f"Recibido: A | Conteo: {contador}")

            # Parpadear LED durante 5 segundos
            start_blink = utime.ticks_ms()
            while utime.ticks_diff(utime.ticks_ms(), start_blink) < 5000:
                led.on()
                utime.sleep(0.25)
                led.off()
                utime.sleep(0.25)

            # Enviar respuesta "B"
            uart.write("B")
            print("Enviado: B")

            # Guardar conteo en archivo
            with open("recibidos.txt", "a") as f:
                f.write(f"{contador}\n")