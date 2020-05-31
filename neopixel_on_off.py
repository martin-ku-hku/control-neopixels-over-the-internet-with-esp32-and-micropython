from machine import Pin
from neopixel import NeoPixel
from time import sleep
import network
import urequests as requests
import ujson

# Wifi credentials
wifi_ssid = "YOUR_WIFI_SSID"
wifi_password = "YOUR_WIFI_PASSWORD"

# Adafruit IO authentication
aio_key = "YOUR_ADAFRUIT_IO_KEY"
username = "YOUR_ADAFRUIT_USERNAME"
headers = {'X-AIO-Key': aio_key, 'Content-Type': 'application/json'}

# Don't forget the NeoPixels!
np = NeoPixel(Pin(15), 12)
feed_names = ['red', 'green', 'blue']
rgb_values = {'red': 0, 'green': 0, 'blue': 0}

# Connect to Wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(wifi_ssid, wifi_password)
while not sta_if.isconnected():
    print(".", end = "")
    
def create_URL(feedname):
    url = "https://io.adafruit.com/api/v2/" + username + "/feeds/" + feedname + "/data/last"
    return url

try:
    while True:
        on_or_off = ujson.loads(requests.get(create_URL('on'), headers=headers).text)['value']
        if on_or_off == 'ON':
            for color in feed_names:
                response = requests.get(create_URL(color), headers=headers)
                parsed = ujson.loads(response.text)
                value = int(parsed['value'])
                rgb_values[color] = value
            for i in range(12):
                np[i] = (rgb_values['red'], rgb_values['green'], rgb_values['blue'])
                np.write()
        else:
            for i in range(12):
                np[i] = (0, 0, 0)
                np.write()
except KeyboardInterrupt:
    for i in range(12):
        np[i] = (0, 0, 0)
        np.write()

