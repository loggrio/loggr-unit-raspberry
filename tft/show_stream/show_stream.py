#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep, strftime
from datetime import datetime
from ConfigParser import ConfigParser
from os import path
import os
import time
import sys
import requests
import logging

HOME_DIR = path.expanduser("~")
CONFIG_FILE = HOME_DIR + '/.loggrrc'

config = ConfigParser()
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
    print 'hello'
    # Check if config file exists
    if not path.isfile(CONFIG_FILE):
        logging.info('Config File not exists')
        return

    config.read(CONFIG_FILE)

    # Check if config file contains options token and userid
    if not config.has_option('STREAMING', 'streaming_pi_ip') or \
       not config.has_option('STREAMING', 'port'):
        logging.info('missing options in config file')
        return

    # Get token and user id from config file
    ip = config.get('STREAMING', 'streaming_pi_ip')
    port = config.get('STREAMING', 'port')


    # Check if ip and port is set
    if not len(ip) or not len(port):
       logging.info('ip or port in config file not set')
       return

    check_stream(ip, port)

if __name__ == '__main__':
    main()
