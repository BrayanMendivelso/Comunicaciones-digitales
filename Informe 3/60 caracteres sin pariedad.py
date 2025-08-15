import machine
import utime
from machine import Pin, UART

led = machine.Pin("LED", machine.Pin.OUT)
uart = UART(0, baudrate=600, bits=8, parity=none, tx=Pin(0), rx=Pin(1))

while True:
    led.on()
    uart.write("A"*60)  
    utime.sleep(1)
    led.off()
    utime.sleep(1)