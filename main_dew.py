# Complete project details at https://RandomNerdTutorials.com
import math


def read_sensor():
    global temp, hum, dew
    temp = hum = dew = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        # if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
        #msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))
        #hum = round(hum, 2)
        # return(msg)
        # else:
        # return('Invalid sensor readings.')
        # dew point formula used: Magnus-Tetens formula (Sonntag90)
        # https://www.omnicalculator.com/physics/dew-point

        def dew_point(t, h):
            a, b = 17.62, 243.12    # Magnus-Tetens constants
            m = math.log(h/100)+a*t/(b+t)
            dp = (b*m)/(a-m)
            return dp
        dew = dew_point(temp, hum)
    except OSError as e:
        return('Failed to read sensor.')


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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

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
