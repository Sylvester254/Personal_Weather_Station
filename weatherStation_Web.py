import network
import socket
from time import sleep
import gc
gc.collect()
from machine import Pin, ADC, I2C 
from PicoDHT22 import PicoDHT22
from bmp085 import BMP180
import time
import utime

ssid = "4G MIFI_F19" #Your network name
password = "1234567890" #Your WiFi password

led_onboard = Pin("LED", Pin.OUT)
i2c = I2C(0, sda = Pin(16), scl = Pin(17), freq = 1000000)

#Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    led_onboard.value(1)
    print('Connecting...')
    sleep(1)
ip = wlan.ifconfig()[0]
print('Connection successful')
print(f'Connected on {ip}')
led_onboard.value(0)

def web_page():

    # init DHT22 on Pin 2(GPIO2)
    dht22 = PicoDHT22(Pin(2, Pin.IN, Pin.PULL_UP))
    led_onboard = Pin("LED", Pin.OUT)
    i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
    Raindrop_AO = ADC(0)        # ADC0 multiplexing pin is GP26 

    T, H = dht22.read()
    
    bmp = BMP180(i2c)
    bmp.oversample = 2
    bmp.sealevel = 101325
    
    temp = bmp.temperature
    press = bmp.pressure
    altitude = bmp.altitude
    temp_f= (temp * (9/5) + 32)
    pressure = "{:.2f}".format(press)
    alti = "{:.2f}".format(altitude)
    
    avg_temp = (T + temp)/2
    avg_temp_f= "{:.2f}".format(avg_temp * (9/5) + 32)
    
    adc_Raindrop = Raindrop_AO.read_u16()
    if adc_Raindrop >= 30000:
        status = 'No rain'
    elif adc_Raindrop >= 10000:
        status = 'Light rain'
    else:
        status = 'Heavy rain'
    

#HTML CODE  
    html = """<html lang="en">

<head>
    <title>Rasp. Pico W Web Server</title>
    <meta http-equiv="refresh" content="10">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
        integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <link rel="icon" href="data:,">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            text-align: center;
        }

        p {
            font-size: 1.2rem;
        }

        body {
            margin: 0;
            background: #4AC29A;  /* fallback for old browsers */
            background: -webkit-linear-gradient(to bottom, #BDFFF3, #4AC29A);  /* Chrome 10-25, Safari 5.1-6 */
            background: linear-gradient(to bottom, #BDFFF3, #4AC29A); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
            

        }

        .topnav {
            overflow: hidden;
            color:#e23b3b;
            font-size: 1.7rem;
            font-family:'Times New Roman', Times, serif;
    
        }

        .content {
            padding: 20px;
        }

        .card {
            border-radius: 9px;
            background-color: white;
            box-shadow: 3px 4px 12px 1px rgba(140, 140, 140, .5);
        }

        .cards {
            max-width: 900px;
            margin: 0 auto;
            display: grid;
            grid-gap: 2rem;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }

        .reading {
            font-size: 2.8rem;
        }

        .card.temperature {
            color: #FF5733; /* bright orange-red */
        }
          
        .card.humidity {
        color: #2E8B57; /* sea green */
        }
        
        .card.pressure {
        color: #888888; /* dark gray */
        }
        
        .card.altitude {
        color: #7B68EE; /* medium purple */
        }
        
        .card.rain {
        color: #73a6db; /* slate gray */
        }
          
    </style>
</head>

<body>
    <div class="topnav">
        <h2>Personal Weather Monitor</h2>
    </div>
    <div class="content">
        <div class="cards">
            <div class="card temperature">
                <h4><i class="fas fa-thermometer-half"></i>TEMP. Celsius</h4>
                <p><span class="reading">""" + str(avg_temp) + """ &#8451; </p>
            </div>
            <div class="card temperature">
                <h4><i class="fas fa-thermometer-half"></i> TEMP. Fahrenheit</h4>
                <p><span class="reading">""" + str(avg_temp_f) + """ &#8457; </p>
            </div>
            <div class="card humidity">
                <h4><i class="fas fa-tint"></i> HUMIDITY</h4>
                <p><span class="reading">""" + str(H) + """ %</p>
            </div>
            <div class="card pressure">
                <h4><i class="fas fa-angle-double-down"></i> PRESSURE</h4>
                <p><span class="reading">""" + str(press) + """ Pa</p>
            </div>
            <div class="card altitude">
                <h4><i class="fas fa-mountain"></i> ALTITUDE</h4>
                <p><span class="reading">""" + str(alti) + """ Meter</p>
            </div>
            <div class="card rain">
                <h4><i class="fas fa-cloud-showers-heavy"></i> RAINFALL</h4>
                <p><span class="reading">""" + str(status) + """ </p>
            </div>
        </div>
    </div>
</body>

</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')
