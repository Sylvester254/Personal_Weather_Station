from machine import Pin, Timer

"""
This code initializes a timer that toggles
the state of the onboard LED connected to
the "LED" pin at a frequency of 2 Hz 
(i.e., the LED will turn on and off every 0.5 seconds).
"""


led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2, mode=Timer.PERIODIC, callback=tick)