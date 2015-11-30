#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, strftime
from datetime import datetime
import os
import time
import sys
import requests
import logging

logging.basicConfig(filename='show_stream.log', level=logging.INFO)
logging.info('Logging (re)started')


def start_stream(stream):
    # example: "DISPLAY=:0.0 vlc -vvv -f http://141.60.125.254:8080/?
    #           action=stream 2>&1 > /tmp/vlc.log"
    try:
        res = os.system(stream)
    except OSError as ose:
        logging.error('OSError: ' + ose.output)
    return res


def check_stream(ip, port):
    http = 'http://'
    action = '/?action=stream'
    stream = http + ip + ':' + port + action
    tft_display = 'DISPLAY=:0.0 '
    vlc_command = 'vlc -vvv -f --play-and-exit '
    error_log = ' 2>&1 > /tmp/vlc.log'
    overall_cmd_show = tft_display + vlc_command + stream + error_log
    isRunning = False
    time = 5
    while(True):
        try:
            # for example 'http://141.60.125.254:8080/?action=stream'
            r = requests.head(http + ip + ':' + port + action)
        except requests.exceptions.ConnectionError as ce:
            print "ConnectionError: Trying again..."
            isRunning = False
            logging.error('Connection Error: ' + ip)
            sleep(time)
            continue

        if r.status_code == requests.codes.ok and isRunning is False:
            start_stream(overall_cmd_show)
            isRunning = True
            sleep(time)

        if r.status_code == 400 and isRunning is False:
            isRunning = True
            start_stream(overall_cmd_show)
            logging.info('Stream (re)started')
            sleep(time)
            continue

        elif r.status_code != requests.codes.ok:
            isRunning = False
            sleep(5)

        elif isRunning is False:
            start_stream(overall_cmd_show)
            logging.info('Stream (re)started')
            isRunning = True


def main():
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    check_stream(ip, port)

if __name__ == '__main__':
    main()
