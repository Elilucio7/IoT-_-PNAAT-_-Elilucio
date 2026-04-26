from machine import Pin
import time

led_pin = Pin(22, Pin.OUT) #led de alerta
bt_alerta_pin = Pin(33, Pin.IN) #botão para acionar alerta definitivo
bt_resfr_pin = Pin(12, Pin.IN) #botão para diminuir a temperatura

temp = 130 #temperatura
flag = False #flag para alarme não parar caso acionado manualmente

print("Teste") #print para evitar erro no github actions

while True: #loop, aumenta temperatura e verifica se há algum botão sendo precionado
    time.sleep(0.1)
    temp += 1
    print(temp)
    if bt_alerta_pin.value() == 0: #ativar alerta sem método de parar sem reiniciar o sistema
        led_pin.value(1)
        flag = True
    elif temp > 140: #ativar alerta de aquecimento
        led_pin.value(1)
    if temp < 120 and flag == False: #desativar alarme quando temperatura estiver abaixo de 120 graus
        led_pin.value(0)
    if bt_resfr_pin.value() == 0: #caso pressionado, o botão de resfriamento irá diminuir a temperatura da máquina
        temp = temp-4