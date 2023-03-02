import time
import network
from machine import Pin, Timer


def light():
    global led
    led = Pin("LED", Pin.OUT)
    tim = Timer()
    def tick(timer):
        global led
        led.toggle()

    tim.init(freq=2, mode=Timer.PERIODIC, callback=tick)



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
    print( 'ip = ' + status[0] )
    light()
