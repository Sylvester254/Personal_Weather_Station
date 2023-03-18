from machine import Pin
from PicoDHT22 import PicoDHT22
import time
import utime

"""This code should continuously read the temperature
    and humidity values and print them to the shell
    with a 10-second delay between each reading.
    It also displays the current time when the readings were recorded
"""

# init DHT22 on Pin 2(GPIO2)
dht22 = PicoDHT22(Pin(2, Pin.IN, Pin.PULL_UP))
while True:
    T, H = dht22.read()
    # Get current time in seconds since the Epoch
    now = utime.time()
    # Convert to a tuple of (year, month, day, hour, minute, second, weekday, yearday)
    time_tuple = utime.gmtime(now)
    # Format the time as a string
    time_str = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4], time_tuple[5])

    print("\nReading at {} : ".format(time_str))
    print("\tTemperature: {} °C".format(T))
    print("\tHumidity: {} %".format(H))
    time.sleep(5)  # wait for 5 seconds before reading again
