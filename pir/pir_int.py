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

GPIO.setmode(GPIO.BCM)
PIR_PIN = 26
GPIO.setup(PIR_PIN, GPIO.IN)

config = ConfigParser()
HOME_DIR = path.expanduser("~")
CONFIG_FILE = HOME_DIR + '/.loggrrc'

PICS_PATH = '/tmp/stream/pic.jpg'

token = ''
userid = ''
containers_url = ''
time_between_pics = 0  # n seconds between pictures
num_pics = 0  # take and send n pictures to webapp after motion detection


def send_pictures():
    # create container
    print containers_url
    print num_pics
    print time_between_pics

    container_name = str(int(time()))
    payload = {'name': container_name}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(containers_url, data=json.dumps(payload),
                          headers=headers)
        print 'Container created'
    except requests.exceptions.ConnectionError as ce:
        log_error('requests failure: ' + str(ce))
        return
    except requests.exceptions.RequestException as re:
        log_error('requests failure: ' + str(re))
        return
    else:
        # send file to container
        i = 0
        while (i < int(num_pics)):
            filename = 'pic' + str(int(time())) + '.jpg'
            files = {'file': (filename, open(PICS_PATH, 'rb'))}
            PICS_URL = containers_url + container_name + '/upload'
            try:
                r = requests.post(PICS_URL, files=files)
                print 'File sent'
                i = i + 1
                sleep(float(time_between_pics))
            except requests.exceptions.ConnectionError as ce:
                log_error('requests failure: ' + str(ce))
                return
            except requests.exceptions.RequestException as re:
                log_error('requests failure: ' + str(re))
                return


# def take_picture():
#     sub_call = ['sudo', 'raspistill', '-vf', '-o']
#     filename = PICS_PATH + time.strftime('%Y%m%d-%H%M%S') + '.jpeg'
#     sub_call.append(filename)
#     subprocess.call(sub_call)
#     log_info('PIR: Took picture')


def motion(PIR_PIN):
    log_info('PIR: Motion detected')
    # take_picture()
    send_pictures()
    sleep(60)  # when detected a motion wait 1 minute to detect another one


def main():
    global token
    global userid
    global containers_url
    global num_pics
    global time_between_pics

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
