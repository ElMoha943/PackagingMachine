from RPi import GPIO
from time import sleep
import requests

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

url = "http://127.0.0.1:5000/"
mac = getserial()

def sendData(metros):
    response = requests.post(url, mac, metros) # mac, metros
    if response.ok:
        print("Upload completed successfully!")
        print(response.text)
    else:
        print("Something went wrong!")
        print(response.text)

# GPIO pins
clk = 17
dt = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                counter2 = 0
        clkLastState = clkState
        sleep(0.0001)
        # if more than 5sec pass without a rotation, send data
        if counter2 > 500:
            metros = counter/1200 # 1200 pulses per meter
            sendData(metros)
            counter = 0 # reset rotation counter
            counter2 = 0
        else:
            counter2 += 1
finally:
    GPIO.cleanup() 

