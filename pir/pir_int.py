#!/usr/bin/python
# pir_int.py
# Detect movement using a PIR module, send pictures to web server

# import required python libraries
import RPi.GPIO as GPIO
from time import time, sleep
import json
from os import path
import subprocess
import logging
import requests
from raspi_loggr.util import log_error
from raspi_loggr.util import log_info
from raspi_loggr.util import treat_missing_config_errors
from raspi_loggr.util import treat_pairing_errors
from ConfigParser import ConfigParser

# use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# use pin 26 (bcm) as input signal pin for PIR module
PIR_PIN = 26
# set pin as input
GPIO.setup(PIR_PIN, GPIO.IN)

# get config file reference
config = ConfigParser()
HOME_DIR = path.expanduser("~")
CONFIG_FILE = HOME_DIR + '/.loggrrc'

PICS_PATH = '/tmp/stream/pic.jpg'

# declare global variables
token = ''
userid = ''
containers_url = ''
time_between_pics = 0  # n seconds between pictures
num_pics = 0  # take and send n pictures to webapp after motion detection


def send_pictures():
    """Send pictures to web server
       {num_pics} pics will be sent, one pic every {time_between_pics}
       seconds
    """
    # create container
    container_name = str(int(time()))
    payload = {'name': container_name}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(containers_url, data=json.dumps(payload),
                          headers=headers)
        print 'Container created'
    except requests.exceptions.ConnectionError as ce:
        # catch and treat requests connection errors
        log_error('requests failure: ' + str(ce))
        return
    except requests.exceptions.RequestException as re:
        # catch and treat requests exceptions
        log_error('requests failure: ' + str(re))
        return
    else:
        # send image files to container
        i = 0
        while (i < int(num_pics)):
            # build file name
            filename = 'pic' + str(int(time())) + '.jpg'
            files = {'file': (filename, open(PICS_PATH, 'rb'))}
            pics_url = containers_url + container_name + '/upload'
            try:
                r = requests.post(pics_url, files=files)
                print 'File sent'
                i = i + 1
                sleep(float(time_between_pics))
            except requests.exceptions.ConnectionError as ce:
                # catch and treat requests connection errors
                log_error('requests failure: ' + str(ce))
                return
            except requests.exceptions.RequestException as re:
                # catch and treat requests exceptions
                log_error('requests failure: ' + str(re))
                return


# def take_picture():
#     sub_call = ['sudo', 'raspistill', '-vf', '-o']
#     filename = PICS_PATH + time.strftime('%Y%m%d-%H%M%S') + '.jpeg'
#     sub_call.append(filename)
#     subprocess.call(sub_call)
#     log_info('PIR: Took picture')


def motion(PIR_PIN):
    """Callback function of event listener on pin 26
       called on rising edge (motion detected by PIR module)

    Args:
        PIR_PIN (int): pin of detected event (rising edge)
    """
    log_info('PIR: Motion detected')
    # take_picture()
    send_pictures()
    sleep(60)  # when detected a motion wait 1 minute to detect another one


def main():
    """Main method of pir_int.py

    1.  Start logging
    2.  Check for valid config file
    3.  Add event listener to pin 26, rising edge, motion() as cb function
    4.  loop
    4a. On rising edge: call motion(), send pics to web server
    """
    # declare variables as global
    global token
    global userid
    global containers_url
    global num_pics
    global time_between_pics

    # start logging into file 'pir.log'
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                        filename='pir.log', level=logging.INFO)
    log_info('PIR-Logging (re)started')

    print 'PIR sensor script (STRG+C to exit)'
    sleep(1)

    # get config data
    # handle config errors
    if not path.isfile(CONFIG_FILE):
        treat_missing_config_errors()
        return

    # read out config file
    config.read(CONFIG_FILE)

    # Check if config file contains options url
    if not config.has_option('AUTH', 'token') or \
       not config.has_option('AUTH', 'userid') or \
       not config.has_option('API', 'url') or \
       not config.has_option('CAMERA', 'num_pics') or \
       not config.has_option('CAMERA', 'time_between_pics'):
        treat_missing_config_errors()
        return

    # Get token and user id from config file
    token = config.get('AUTH', 'token')
    userid = config.get('AUTH', 'userid')
    containers_url = config.get('API', 'url') + 'containers/'

    num_pics = config.get('CAMERA', 'num_pics')
    time_between_pics = config.get('CAMERA', 'time_between_pics')

    # Check if token and userid is set
    if not len(token) or not len(userid):
        treat_pairing_errors()
        return

    # Check if url is set
    if not len(containers_url) or not len(num_pics) or \
       not len(time_between_pics):
        treat_missing_config_errors()
        return

    print 'Ready'
    try:
        # Add listener to gpio pin 26 to detect rising edge
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
        while 1:
            sleep(3)
    except KeyboardInterrupt:
        print 'Exit'
        GPIO.cleanup()


if __name__ == "__main__":
    main()
