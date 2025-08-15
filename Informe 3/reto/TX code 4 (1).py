import machine
import utime
from machine import Pin, UART

# === CONFIGURACIÓN ===
LED_FIJO = 15      # LED que queda encendido fijo cuando es mi turno de enviar
LED_TITILA = 14    # LED que titila cuando estoy recibiendo
MI_CARACTER = "B"  # Cambiar a "B" en el otro dispositivo
PERIODO = 0.5        # Segundos que dura cada fase

# Configuración LEDs
led_fijo = Pin(LED_FIJO, Pin.OUT)
led_titila = Pin(LED_TITILA, Pin.OUT)

# Configuración UART
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

while True:
    # === 1. Enviar mi carácter ===
    led_fijo.on()  # Enciendo LED fijo mientras envío
    uart.write(MI_CARACTER)
    print(f"Enviado: {MI_CARACTER}")

    start_time = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start_time) < PERIODO * 1000:
        # Escuchar mientras es mi turno
        if uart.any():
            dato = uart.read(1)
            if dato:
                print(f"Recibido: {dato.decode()}")
                # Titilar LED de actividad al recibir algo
                led_titila.on()
                utime.sleep(0.1)
                led_titila.off()
        utime.sleep(0.05)

    led_fijo.off()

    # === 2. Ahora el otro envía, yo recibo ===
    start_time = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start_time) < PERIODO * 1000:
        if uart.any():
            dato = uart.read(1)
            if dato:
                print(f"Recibido: {dato.decode()}")
                # Titilar LED de actividad (ahora recibo)
                led_titila.on()
                utime.sleep(0.1)
                led_titila.off()
        utime.sleep(0.05)

    # Alternar carácter para que siempre sea A-B-A-B...
    MI_CARACTER = "B" if MI_CARACTER == "A" else "A"

