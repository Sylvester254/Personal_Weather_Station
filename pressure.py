from time import sleep
from machine import Pin, I2C
from bmp085 import BMP180
"""
Reads pressure, temperature and altitude which is calculated from
measured pressure and sealevel pressure(101325Pa)

- I'm using BMP085 library
"""


led_onboard = Pin("LED", Pin.OUT)
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)


while True:
    #Sensor Configuration
    bmp = BMP180(i2c)
    bmp.oversample = 2
    bmp.sealevel = 101325
    
    temp = bmp.temperature
    press = bmp.pressure
    altitude = bmp.altitude
    temp_f= (temp * (9/5) + 32)
    pressure = "{:.2f}".format(press)
    alti = "{:.2f}".format(altitude)
    
    print(" ********************************")
    print(" Temperature:  {} °C".format(temp))
    print(" Temperature:  {} F".format(temp_f))
    print("Atm. Pressure: {} hPa".format(pressure))
    print(" Altitude: {} meters".format(alti))

    sleep(5)  # wait for 5 seconds before reading again

