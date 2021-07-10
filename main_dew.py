# Extenstion to the previous exercise with a dew point subroutine added
# boot.py is same which setup wifi connection

# This file is used to create a webserver in esp32 which serve a webpage with temperature and humidity readings
# from a dht11 sensor. The webpage can be accessed over wifi with the ip address.

# Import math library
import math

# function to read temperature and humidity data


def read_sensor():
    global temp, hum, dew
    temp = hum = dew = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
# dew point calculation from measured temperature and humidity
# dew point formula used: Magnus-Tetens formula (Sonntag90)
# ref. https://www.omnicalculator.com/physics/dew-point

        def dew_point(t, h):
            a, b = 17.62, 243.12    # Magnus-Tetens constants
            m = math.log(h/100)+a*t/(b+t)
            dp = (b*m)/(a-m)
            return dp
        dew = dew_point(temp, hum)
    except OSError as e:
        return('Failed to read sensor.')


# function to return the HTML page
# display table with two rows and two columns
def web_page():
    html = """<!DOCTYPE HTML><html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
       body {
         font-family: Arial, Helvetica, sans-serif;
       }
        th, td {
        text-align: left;
        padding:0 0 0 20px;
        font-weight: bold;
        }
        table.center {
        margin-left: auto;
        margin-right: auto;
        }
        h2 {
        text-align: center
        }
       
     </style>
</head>
<body>
  <h2>ESP32 Mittaukset</h2>
     <table class="center">
        <tr>
           <td>Lämpötila &nbsp; &nbsp;   </td>
           <td> <span>"""+str(temp)+"""</span> <span>&#8451;</span></td>
        </tr>
        <tr>
           <td>Kosteus</td>
           <td>"""+str(hum)+""" <span>&#37;</span> </td>
        </tr>
        <tr>
           <td>Dew Point</td>
           <td>"""+str(dew)+""" <span>&#8451;</span> </td>
        </tr>
     </table>
</html>"""
    return html


# create webserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))  # bind socket to address and port
s.listen(5)

# listen for requests and send response
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    sensor_readings = read_sensor()
    print(sensor_readings)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
