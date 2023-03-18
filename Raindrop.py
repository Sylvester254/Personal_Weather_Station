from machine import Pin,ADC,PWM,I2C 
import time
 """
If the ADC value is greater than or equal to 40000, it's interpreted as no rain.
If the ADC value is between 30000 and 40000, it's interpreted as light rain.
If the ADC value is less than 30000, it's interpreted as heavy rain.
"""
 
 
Raindrop_AO = ADC(0)        # ADC0 multiplexing pin is GP26               
 
# def setup():
    
def loop():
    while True:
        adc_Raindrop = Raindrop_AO.read_u16()
        print('\n**********************')
        if adc_Raindrop >= 30000:
            print('No rain')
            print(adc_Raindrop)
        elif adc_Raindrop >= 10000:
            print('Light rain')
            print(adc_Raindrop)
        else:
            print('Heavy rain')
            print(adc_Raindrop)
        time.sleep(5)
if __name__ == '__main__':
  #  setup()
    loop()