from flask import Flask, render_template
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import os

counter = 22

GpioPins = [6,13,19,26]

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT)

mymotortest = RpiMotorLib.BYJMotor("MyMotorOne","28BYJ")

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html',treats_remaining = counter)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/dispense/')

def dispense():
    global counter
    counter = counter - 1
    print(counter)
    #dispense.y
    print("dispensing")
    mymotortest.motor_run(GpioPins, 0.001,42,True,False,"half",0.001)
  #  print(dispense.y)
   # dispense.y = dispense.y+1
    return render_template('home.html',treats_remaining = counter)
   
    
    
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='192.168.1.1', port=443, debug=False)
#
#https://alvarotrigo#.com/blog/10-cool-css-animations-to-add-to-your-website/
#
