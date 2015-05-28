#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import logging
from enum import Enum


class LedStatusTypes(Enum):
    ok = 1  # green
    sensor_broken = 2  # red
    request_error = 3  # orange


class SensorTypes(Enum):
    temperature = 1
    brightness = 2
    humidity = 3
    volume = 4
    pressure = 5


class ValueUnits(Enum):
    grad_celsius = 1
    grad_fahrenheit = 2
    percent = 3
    lumen = 4
    decibel = 5
    pascal = 6


def set_status_led(status):
    command = ['sensors/rgb.out', str(status)]
    try:
        subproc = subprocess.check_call(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    except subprocess.CalledProcessError, cpe:
        if cpe.returncode == 1:
            # catch invalid arguments errors
            logging.error('called process error: ' + str(cpe.cmd[0]) + ' returned 1: invalid arguments')
            print 'called process error: ' + str(cpe.cmd[0]) + ' returned 1: invalid arguments'
        elif cpe.returncode == 2:
            # catch wiringPi errors
            logging.error('called process error: ' + str(cpe.cmd[0]) + ' returned 2: setup wiringPi failed')
            print 'called process error: ' + str(cpe.cmd[0]) + ' returned 2: setup wiringPi failed'
    except OSError, ose:
        # catch os errors, e.g. file-not-found
        logging.error('oserror: ' + str(ose.strerror))
        print 'oserror: ' + str(ose.strerror)
