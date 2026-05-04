from machine import Pin, I2C
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
oled = SSD1306_I2C(oled_width, oled_height, i2c) #oled

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

#classe do ssd1306, o github Actions não está programado para um arquivo além do .py, portanto foi necessário colar o import para a main

SET_CONTRAST        = const(0x81)
SET_ENTIRE_ON       = const(0xa4)
SET_NORM_INV        = const(0xa6)
SET_DISP            = const(0xae)
SET_MEM_ADDR        = const(0x20)
SET_COL_ADDR        = const(0x21)
SET_PAGE_ADDR       = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP       = const(0xa0)
SET_MUX_RATIO       = const(0xa8)
SET_COM_OUT_DIR     = const(0xc0)
SET_DISP_OFFSET     = const(0xd3)
SET_COM_PIN_CFG     = const(0xda)
SET_DISP_CLK_DIV    = const(0xd5)
SET_PRECHARGE       = const(0xd9)
SET_VCOM_DESEL      = const(0xdb)
SET_CHARGE_PUMP     = const(0x8d)
class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        # Note the subclass must initialize self.framebuf to a framebuffer.
        # This is necessary because the underlying data buffer is different
        # between I2C and SPI implementations (I2C needs an extra byte).
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00, # off
            # address setting
            SET_MEM_ADDR, 0x00, # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
            SET_VCOM_DESEL, 0x30, # 0.83*Vcc
            # display
            SET_CONTRAST, 0xff, # maximum
            SET_ENTIRE_ON, # output follows RAM contents
            SET_NORM_INV, # not inverted
            # charge pump
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_framebuf()

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        # Add an extra byte to the data buffer to hold an I2C data/command byte
        # to use hardware-compatible I2C transactions.  A memoryview of the
        # buffer is used to mask this byte from the framebuffer operations
        # (without a major memory hit as memoryview doesn't copy to a separate
        # buffer).
        self.buffer = bytearray(((height // 8) * width) + 1)
        self.buffer[0] = 0x40  # Set first byte of data buffer to Co=0, D/C=1
        self.framebuf = framebuf.FrameBuffer1(memoryview(self.buffer)[1:], width, height)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_framebuf(self):
        # Blast out the frame buffer using a single I2C transaction to support
        # hardware I2C interfaces.
        self.i2c.writeto(self.addr, self.buffer)

    def poweron(self):
        pass