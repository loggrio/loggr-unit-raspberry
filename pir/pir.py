#!/usr/bin/Python
# pir.py
# Detect movement using a PIR module

# Import required Python libraries
import RPi.GPIO as GPIO
import time
import subprocess

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi (BCM)
GPIO_PIR = 26 # BCM 26 = wiringPi-Pin 25

print "PIR Module Test (CTRL-C to exit)"

# Set pin as input
GPIO.setup(GPIO_PIR, GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0

try:
    print "Waiting for PIR to settle ..."
    # Loop until PIR output is 0
    while GPIO.input(GPIO_PIR) == 1:
        Current_State = 0
    print "  Ready"
    # Loop until users quits with CTRL-C
    while True :
        # Read PIR state
        Current_State = GPIO.input(GPIO_PIR)
        if Current_State == 1 and Previous_State == 0:
            print "  Motion detected!"
            # Start raspistill to take a picture
            cam_call = ['raspistill', '-vf', '-o']
            filename = '../pics/' + time.strftime('%Y%m%d-%H%M%S') + '.jpeg'
            cam_call.append(filename)
            # Take a pic and save it to pics folder
            subprocess.call(cam_call)
            # Record previous state
            Previous_State = 1
        elif Current_State == 0 and Previous_State == 1:
            # PIR has returned to ready state
            print "  Ready"
            Previous_State = 0
        # Wait for 10 milliseconds
        time.sleep(0.01)

except KeyboardInterrupt:
    print "  Quit"
    # Reset GPIO settings
    GPIO.cleanup()
