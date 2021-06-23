from rpi_backlight import Backlight
import smbus
import time

I2C_CH = 1
BH1750_DEV_ADDR = 0x23
CONT_H_RES_MODE = 0x10
CONT_H_RES_MODE2 = 0x11
CONT_L_RES_MODE = 0x13
ONETIME_H_RES_MODE = 0x20
ONETIME_H_RES_MODE2 = 0x21
ONETIME_L_RES_MODE = 0x23

backlight = Backlight()

while True:
    i2c = smbus.SMBus(I2C_CH)
    luxBytes = i2c.read_i2c_block_data(BH1750_DEV_ADDR, CONT_H_RES_MODE, 2)
    lux = int.from_bytes(luxBytes, byteorder = 'big')
    print('{0} light'.format(lux))
    value = backlight.brightness
    if value >= 11 and value <= 100:
        if lux >= 200 and lux <= 300:
            backlight.brightness=75
        elif lux >= 100 and lux <= 200:
            backlight.brightness=50
        elif lux >=0 and lux <= 100:
            backlight.brightness=25
        else:
            backlight.brightness=100
    time.sleep(10)
        





    
    
    
    

