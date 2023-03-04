import network
import urequests
import time
from machine import Pin
from PicoDHT22 import PicoDHT22


"""
    Sends the DHT22 sensor data to My-Server using an HTTP POST
    request to this endpoint: (https://127.0.0.1:5000/index). 
    Note that we're using the urequests module to send the HTTP POST request.
    ****
        Has access issues for now. Sample response at rshell:
            waiting for connection...
            connected
            ip = 192.168.100.103

            Reading: 
            Temperature: 28.0 °C
            Humidity: 65.3 %
            Error: [Errno 113] EHOSTUNREACH
    ****
"""


def dht22():
    # init DHT22 on Pin 2(GPIO2)
    dht22 = PicoDHT22(Pin(2, Pin.IN, Pin.PULL_UP))

    # Endpoint for sending sensor data
    url = "https://127.0.0.1:5000/dht22"

    while True:
        try:
            # Read temperature and humidity from DHT22
            temperature, humidity = dht22.read()

            print("\n Reading: ")
            print("Temperature: {} °C".format(temperature))
            print("Humidity: {} %".format(humidity))

            data = {
                "temperature": temperature,
                "humidity": humidity,
            }

            # Send POST request to server
            response = urequests.post(url, json=data)

            # response status code
            print("Response code:", response.status_code)

            time.sleep(10)

        except Exception as e:
            print("Error:", e)
        time.sleep(10)


# Initialize the Wi-Fi connection
ssid = '4G MIFI_F19'
password = '1234567890'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:

    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    dht22()