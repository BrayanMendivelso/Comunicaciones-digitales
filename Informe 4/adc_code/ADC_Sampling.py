import machine
import utime
from machine import Pin, UART

led = machine.Pin("LED", machine.Pin.OUT)
uart = UART(5, baudrate=4800, bits=8, parity=5, tx=Pin(0), rx=Pin(1), stop=1)

while True:
    led.on()
    uart.write("Teleco2025")
    utime.sleep(1)
    led.off()
    utime.sleep(1)

