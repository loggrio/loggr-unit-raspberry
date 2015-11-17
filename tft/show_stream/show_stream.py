#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import *
from time import sleep, strftime
from datetime import datetime
import time
import sys
import requests
import logging

logging.basicConfig(filename='show_stream.log',level=logging.DEBUG)
isBroken = True

def run_cmd(stream):
    tft_display = 'DISPLAY=:0.0 '
    vlc_command = 'vlc -vvv -f '
    log = ' 2>&1 > /tmp/vlc.log'
    # for example "DISPLAY=:0.0 vlc -vvv -f http://141.60.125.254:8080/?action=stream 2>&1 > /tmp/vlc.log"
    cmd_show = tft_display + vlc_command + stream + log
    try:
        p = Popen(cmd_show, shell=True, stdout=PIPE)
        output = p.communicate()[0]
    except OSError as e:
        logging.info('Start VLC Error: ' + e.output)
    return output


def check_stream(ip,port):
    http = 'http://'
    action = '/?action=stream'
    stream = http + ip + ':' + port + action
    while(True):
        try:
            # for example 'http://141.60.125.254:8080/?action=stream'
            r = requests.get(stream  , timeout=0.005)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            isBroken = True
            logging.info('Timeout Error: ' + ip)
            sleep(30)
            continue

        if r.status_code != requests.codes.ok:
            isBroken = True
            logging.info('Request Code not ok')
            sleep(30)
            continue

        elif isBroken is True:
            run_cmd(stream)
            logging.info('Start Stream')
            isBroken = False


def main():
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    check_stream(ip,port)

if __name__ == '__main__':
    main()
