from machine import Pin, I2C
import ssd1306
import onewire
import ds18x20
import time

led_temp_pin = Pin(23, Pin.OUT) #led de alerta
led_evac_pin = Pin(19, Pin.OUT) #led de evacuação
bt_alert_pin = Pin(32, Pin.IN) #botão para acionar alerta definitivo
bt_frz_pin = Pin(13, Pin.IN) #botão para diminuir a temperatura

i2c = I2C(0, scl=Pin(22), sda=Pin(21)) #pin do oled
oled_width = 128 #largura do oled
oled_height = 64 #altura do oled
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c) #oled

ow = onewire.OneWire(Pin(14)) #conectando pino ao sensor
temp_sensor = ds18x20.DS18X20(ow) #sensor de temperatura
roms = temp_sensor.scan() #ROM address para encontrar o sensor

def read_temp(): #leitura da temperatura no sensor
    if not roms: #caso não haja sensor
        return None
    try:
      temp_sensor.convert_temp() #medição da temperatura
      time.sleep_ms(750) #espera para completar o processo
      return temp_sensor.read_temp(roms[0]) #retorna a leitura do sensor
    except Exception as e: #para erro de leitura
      return None

print("Teste") #print para evitar erro no github actions 

while True: #loop do programa
  time.sleep(1)
  temp = read_temp()
  while temp is None: #caso haja erro de leitura, repete-a até conseguir o valor
    temp = read_temp()

  if bt_alert_pin.value() == 0: #ativar alerta sem método de parar além de reiniciar o sistema
    led_evac_pin.value(1)
    led_temp_pin(0)
    oled.fill(0) #limpar display do oled
    oled.text(f"ALERT ACTIVATED", 0, 0) #atualizar texto
    oled.show()
    break
  
  if temp > 99 and temp <125: #ativar alerta de aquecimento
    led_temp_pin.value(1)
    led_evac_pin.value(0)
    oled.fill(0)
    oled.text(f"HIGH TEMP: {temp}", 0, 0)

  if temp == 125 or temp > 125: #ativar alarme de temperatura muito elevada
    led_temp_pin.value(1)
    led_evac_pin.value(1)
    oled.fill(0)
    oled.text(f"ALERT, HIGH TEMP", 0, 0)
  
  if temp < 100: #desativar alarme quando temperatura estiver abaixo de 100 graus
    led_temp_pin.value(0)
    led_evac_pin(0)
    oled.fill(0)
    oled.text(f"{temp}" , 0, 0)
  
  oled.show() #mostrar texto no display
