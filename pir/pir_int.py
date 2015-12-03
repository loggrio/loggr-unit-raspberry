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

# PICS_PATH = '/home/pi/Coding/loggr.io/raspi/pics/'
PICS_PATH = '/tmp/stream/pic.jpg'
CONTAINERS_URL = 'http://0.0.0.0:3000/api/containers/'

NUM_PICS = 5  # take and send 5 pictures to webapp after motion detection
TIME_BETWEEN_PICS = 2  # 2 seconds between pictures


def send_pictures():
    # create container
    container_name = str(int(time()))
    payload = {'name': container_name}
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(CONTAINERS_URL, data=json.dumps(payload),
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
        while (i < NUM_PICS):
            filename = 'pic' + str(int(time())) + '.jpg'
            files = {'file': (filename, open(PICS_PATH, 'rb'))}
            PICS_URL = CONTAINERS_URL + container_name + '/upload'
            try:
                r = requests.post(PICS_URL, files=files)
                print 'File sent'
                i = i + 1
                sleep(TIME_BETWEEN_PICS)
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
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                        filename='pir.log', level=logging.INFO)
    log_info('PIR-Logging (re)started')

    print 'PIR sensor script (STRG+C to exit)'
    sleep(1)

    # get config data
    # handle config errors
    # if not path.isfile(CONFIG_FILE):
    #     treat_missing_config_errors()
    #     return
    #
    # config.read(CONFIG_FILE)
    #
    # # Check if config file contains options url
    # if not config.has_option('AUTH', 'token') or \
    #    not config.has_option('AUTH', 'userid') or \
    #    not config.has_option('CAMERA', 'url'):
    #     treat_missing_config_errors()
    #     return
    #
    # # Get token and user id from config file
    # token = config.get('AUTH', 'token')
    # userid = config.get('AUTH', 'userid')
    # url = config.get('CAMERA', 'url')
    #
    # # Check if token and userid is set
    # if not len(token) or not len(userid):
    #     treat_pairing_errors()
    #     return
    #
    # # Check if url is set
    # if not len(url):
    #     treat_missing_config_errors()
    #     return

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
