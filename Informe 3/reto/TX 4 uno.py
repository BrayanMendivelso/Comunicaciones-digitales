import machine
import utime
from machine import Pin, UART

# LED en GP15
led = Pin(15, Pin.OUT)

# UART
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

while True:
    # 1. Enviar "A" cada 2 segundos
    uart.write("A")
    print("Enviado: A")
    utime.sleep(0.5)

    # 2. Esperar respuesta
    start_wait = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start_wait) < 1000:  # Espera hasta 1 segundo
        if uart.any():
            dato = uart.read(1)
            if dato == b"B":
                print("Recibido: B")
                # Parpadear LED durante 3 segundos
                start_blink = utime.ticks_ms()
                while utime.ticks_diff(utime.ticks_ms(), start_blink) < 3000:
                    led.on()
                    utime.sleep(0.25)
                    led.off()
                    utime.sleep(0.25)
                break
