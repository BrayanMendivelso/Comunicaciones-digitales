import machine
import utime
from machine import Pin, UART

# === CONFIGURACIÓN ===
LED_ACCION = 15  # LED que parpadea según el carácter recibido
LED_ACTIVIDAD = 14  # LED que indica cualquier envío o recepción
MI_CARACTER = "A"   # En un dispositivo pones "A", en el otro "B"
PERIODO_ENVIO = 0.5   # Segundos entre envíos

# Configuración LEDs
led_accion = Pin(LED_ACCION, Pin.OUT)
led_actividad = Pin(LED_ACTIVIDAD, Pin.OUT)

# Configuración UART
uart = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

ultimo_envio = utime.ticks_ms()

while True:
    # === 1. Enviar mi carácter cada PERIODO_ENVIO segundos ===
    if utime.ticks_diff(utime.ticks_ms(), ultimo_envio) >= PERIODO_ENVIO * 1000:
        uart.write(MI_CARACTER)
        print(f"Enviado: {MI_CARACTER}")
        # LED de actividad encendido breve para indicar envío
        led_actividad.on()
        utime.sleep(0.05)
        led_actividad.off()
        ultimo_envio = utime.ticks_ms()

    # === 2. Leer cualquier dato entrante y reaccionar ===
    if uart.any():
        dato = uart.read(1)
        if dato:
            recibido = dato.decode()
            print(f"Recibido: {recibido}")

            # LED de actividad encendido breve para indicar recepción
            led_actividad.on()
            utime.sleep(0.05)
            led_actividad.off()

            # Parpadeo según lo recibido en LED de acción (GP15)
            if recibido == "A":
                start_blink = utime.ticks_ms()
                while utime.ticks_diff(utime.ticks_ms(), start_blink) < 5000:
                    led_accion.toggle()
                    utime.sleep(0.25)
                led_accion.off()
            elif recibido == "B":
                start_blink = utime.ticks_ms()
                while utime.ticks_diff(utime.ticks_ms(), start_blink) < 3000:
                    led_accion.toggle()
                    utime.sleep(0.25)
                led_accion.off()

    utime.sleep(0.02)  # Pequeña pausa para no saturar CPU

