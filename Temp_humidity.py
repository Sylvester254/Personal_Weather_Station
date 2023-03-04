from machine import Pin
from PicoDHT22 import PicoDHT22
import time

"""This code should continuously read the temperature
    and humidity values and print them to the console
    with a 5-second delay between each reading
"""


# init DHT22 on Pin 2(GPIO2)
dht22 = PicoDHT22(Pin(2,Pin.IN,Pin.PULL_UP))
while True:
    T, H = dht22.read()
    print("\n Reading: ")
    print("Temperature: {} °C".format(T))
    print("Humidity: {} %".format(H))
    time.sleep(5)  # wait for 5 seconds before reading again