from machine import Pin
import time

led_pin = Pin(22, Pin.OUT)
bt_alerta_pin = Pin(33, Pin.IN)
bt_resfr_pin = Pin(12, Pin.IN)

temp = 130
flag = False

while True:
    time.sleep(0.1)
    temp += 1
    print(temp)
    if bt_alerta_pin.value() == 0:
        led_pin.value(1)
        flag = True
    elif temp > 140:
        led_pin.value(1)
    if temp < 120 and flag == False:
        led_pin.value(0)
    if bt_resfr_pin.value() == 0:
        temp = temp-4