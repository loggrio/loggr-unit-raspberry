#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen,PIPE
from time import sleep, strftime
from datetime import datetime
import os
import time
import sys
import requests
import logging

logging.basicConfig(filename='show_stream.log', level=logging.DEBUG)



def run_cmd(cmd):

    # example: "DISPLAY=:0.0 vlc -vvv -f http://141.60.125.254:8080/?
    #           action=stream 2>&1 > /tmp/vlc.log"

    try:
        resultcode = os.system(cmd)
    except OSError as e:
        logging.info('Start VLC Error: ' + e.output)
    return resultcode


def check_stream(ip, port):
    http = 'http://'
    action = '/?action=stream'
    stream = http + ip + ':' + port + action
    tft_display = 'DISPLAY=:0.0 '
    vlc_command = 'vlc -vvv -f --play-and-exit '
    error_log = ' 2>&1 > /tmp/vlc.log'
    cmd_show = tft_display + vlc_command + stream + error_log
    kill = 'sudo killall vlc'
    isBroken = True
    time = 5
    while(True):
        try:
            # for example 'http://141.60.125.254:8080/?action=stream'
            print "vor request"
            r = requests.head('http://141.60.131.238:8080/?action=stream')
            print r
            print "nach request"
        except (requests.exceptions.ConnectionError):
            print "ConnectionError try again"
            isBroken = True
            logging.info('Connection Error: ' + ip)
            sleep(time)
            continue


        if r.status_code == requests.codes.ok and isBroken == True:
            run_cmd(cmd_show)
            isBroken = False
            sleep(time)
            #debugging

            #r.status_code = 400
        if r.status_code == 400 and isBroken == True:
            isBroken = False
            run_cmd(cmd_show) #debug
            logging.info('Request Code not ok')
            sleep(time)
            continue

        elif r.status_code != requests.codes.ok:
            isBroken = True
            sleep(5)


        elif isBroken is True:
            run_cmd(cmd_show)
            logging.info('Start Stream')
            isBroken = False



def main():
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    check_stream(ip, port)

if __name__ == '__main__':
    main()
