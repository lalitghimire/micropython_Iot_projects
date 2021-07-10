# This file is used to create a webserver in esp32 which serve a webpage with temperature and humidity readings
# from a dht11 sensor. The webpage can be accessed over wifi with the ip address.


# function to read temperature and humidity data
def read_sensor():
    global temp, hum  # created global variable to store read data
    temp = hum = 0
    # import the data
    # try and exception is useful to prevent the web server from crashing when  not able to read from the sensor
    try:
        sensor.measure()  # invoke measure method in sensor
        temp = sensor.temperature()
        hum = sensor.humidity()

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
     </table>
</html>"""
    return html


# create webserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
s.bind(('', 80))  # bind socket to address and port
s.listen(5)  # accept connection. max is 5 connection
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
