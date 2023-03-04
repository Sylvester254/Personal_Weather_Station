from machine import Pin
from PicoDHT22 import PicoDHT22
import time


# init DHT22 on Pin 2(GPIO2)
dht22 = PicoDHT22(Pin(2,Pin.IN,Pin.PULL_UP))
while True:
    T, H = dht22.read()
    print("\n Reading: ")
    print("Temperature: {} °C".format(T))
    print("Humidity: {} %".format(H))
    time.sleep(5)  # wait for 5 seconds before reading again