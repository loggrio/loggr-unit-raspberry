import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

def motion(PIR_PIN):
    print 'Motion detected'
    sub_call = ['raspistill', '-vf', '-o']
    filename = '../pics/' + time.strftime('%Y%m%d-%H%M%S') + '.jpeg'
    sub_call.append(filename)
    subprocess.call(sub_call)

print 'PIR Testscript (STRG+C to exit)'
time.sleep(1)
print 'Ready'
try:
    # Add listener to gpio pin 26 to detect rising edge
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
    while 1:
        time.sleep(3)
except KeyboardInterrupt:
    print 'Exit'
    GPIO.cleanup()
