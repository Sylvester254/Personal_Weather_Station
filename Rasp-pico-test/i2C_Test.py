from machine import Pin, I2C
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
devices = i2c.scan()
print(devices)
