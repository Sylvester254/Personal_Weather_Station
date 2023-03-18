from machine import Pin, ADC, I2C 
from PicoDHT22 import PicoDHT22
from bmp085 import BMP180
import time
import utime


"""This function should continuously read the temperature
    and humidity values with a 10-second delay between each reading.
    It also displays the current time when the readings were recorded
"""


def temp():
    # init DHT22 on Pin 2(GPIO2)
    dht22 = PicoDHT22(Pin(2, Pin.IN, Pin.PULL_UP))
    while True:
        T, H = dht22.read()
        #time.sleep(10)
        return T, H


"""
pressure function reads pressure, temperature, and altitude which is calculated from
measured pressure, temperature and sealevel pressure(101325Pa)
"""


def pressure():
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
        
        #time.sleep(10)
        return temp, temp_f, press, altitude


"""
Raindrop function:
If the ADC value is greater than or equal to 40000, it's interpreted as no rain.
If the ADC value is between 30000 and 40000, it's interpreted as light rain.
If the ADC value is less than 30000, it's interpreted as heavy rain.
"""
 
 
def rain():
    Raindrop_AO = ADC(0)        # ADC0 multiplexing pin is GP26               
    while True:
        adc_Raindrop = Raindrop_AO.read_u16()
        
        #time.sleep(10)
        return adc_Raindrop

if __name__ == '__main__':
    
    while True:
        # Get current time in seconds since the Epoch
        now = utime.time()
        # Convert to a tuple of (year, month, day, hour, minute, second, weekday, yearday)
        time_tuple = utime.gmtime(now)
        # Format the time as a string
        time_str = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4], time_tuple[5])

        temp_val = temp()
        pressure_val = pressure()
        rain_val = rain()
        
        
        print("\n\t\tValues obtained at {} : ".format(time_str))
        print('**********DHT22************')
        print("Temperature: {} °C".format(temp_val[0]))
        print("Humidity: {} %".format(temp_val[1]))
        
        print('**********BMP180************')
        print("Temperature:  {} °C".format(pressure_val[0]))
        print("Temperature:  {} F".format(pressure_val[1]))
        print("Atm. Pressure: {} hPa".format(pressure_val[2]))
        print("Altitude: {} meters".format(pressure_val[3]))
        
        adc_Raindrop = rain_val
        
        print('**********RAINDROP************')
        if adc_Raindrop >= 40000:
            print('No rain')
            print(adc_Raindrop)
        elif adc_Raindrop >= 25000:
            print('Light rain')
            print(adc_Raindrop)
        else:
            print('Heavy rain')
            print(adc_Raindrop) 
        time.sleep(10)  # wait for 10 seconds before reading again
