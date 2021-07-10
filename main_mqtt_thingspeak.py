
import math
# MQTT library for micropython
from umqtt.simple import MQTTClient
import time

# function to read sensor data, calculate dew point and assign to variables
def read_sensor():
    global temp, hum, dew
    temp = hum = dew = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        def dew_point(t, h):
            a, b = 17.62, 243.12    # Magnus-Tetens constants
            m = math.log(h/100)+a*t/(b+t)
            dp = (b*m)/(a-m)
            return dp
        dew = dew_point(temp, hum)
    except OSError as e:
        return('Failed to read sensor.')


# Thingspeak setup:
SERVER = "mqtt.thingspeak.com"
client = MQTTClient("umqtt_client", SERVER)
CHANNEL_ID = "*******"  # Thingspeak channel id
WRITE_API_KEY = "*******"  # Own Api key from thingspeak.com for the channel id
# topic = "channels/1249898/publish/PJX6E1D8XLV18Z87"
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY
UPDATE_TIME_INTERVAL = 30000  # in ms unit
last_update = time.ticks_ms()

# Main loop to publish data to thingspeak at an update interval
while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        read_sensor()
        #payload = "field1=" + str(t) + "&field2=" + str(h)
        payload = "field1={}&field2={}&field3={}" .format(
            str(temp), str(hum), str(dew))
        client.connect()
        client.publish(topic, payload)
        client.disconnect()

        print(payload)
        # update time
        last_update = time.ticks_ms()
