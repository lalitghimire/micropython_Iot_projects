# Complete project details at https://RandomNerdTutorials.com

try:
import gc
import usocket as socket
except:
    import socket

import network
from machine import Pin
import dht

import esp
esp.osdebug(None)

gc.collect()

ssid = 'LG'
password = 'Ghimire963852741'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

#sensor = dht.DHT22(Pin(14))
sensor = dht.DHT11(Pin(14))