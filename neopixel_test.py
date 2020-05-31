from machine import Pin
from neopixel import NeoPixel
from time import sleep

np = NeoPixel(Pin(15), 12)
      
try:
    while True:
        for i in range(12):
            np[i] = (255, 0, 0)
            np.write()
        sleep(1)
        for i in range(12):
            np[i] = (0, 0, 0)
            np.write()
        sleep(1)
except KeyboardInterrupt:
    for i in range(12):
        np[i] = (0, 0, 0)
        np.write()