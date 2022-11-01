#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os
from RpiMotorLib import RpiMotorLib
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.1.1'  # IP Address of Raspberry Pi
host_port = 443
x = 50

GpioPins = [6,13,19,26]
def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT)

mymotortest = RpiMotorLib.BYJMotor("MyMotorOne","28BYJ")

def getTemperature():
    tempb = os.popen("/usr/bin/vcgencmd measure_temp").read()
    return tempb
    

class MyServer(BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto; color:purple">
           <h1>Welcome to the Kitty 3000</h1>
           <p>Current GPU temperature of the pi is: {}</p>
           <progress max="100" value=<var>x<var>>40%</progress>
           <form action="/" method="POST">
               Dispense :
               <input type="submit" name="submit" value="On">
               <input type="submit" name="submit" value="Off">
           </form>
           </body>
           </html>
        '''
        temp = getTemperature()
     
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:]).encode("utf-8"))
        self.wfile.write(html.format(y[1]).encode("utf-8"))
        
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]
        

        setupGPIO()

        if post_data == 'On':
            GPIO.output(18, GPIO.HIGH)
            mymotortest.motor_run(GpioPins, 0.001,100,False,False,"half",0.001)
            
        else:
            GPIO.output(18, GPIO.LOW)
            

        print("LED is {}".format(post_data))
    
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
  
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
