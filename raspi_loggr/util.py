#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import logging
from enum import Enum


class LedStatusTypes(Enum):
    ok = 1  # green
    sensor_broken = 2  # red
    request_error = 3  # orange
    pairing_succeeded = 4  # blue


class SensorTypes(Enum):
    temperature = 1
    brightness = 2
    humidity = 3
    pressure = 4


def log_info(info):
    logging.info(info)
    print info


def log_error(err):
    logging.error(err)
    print err


def treat_sensor_errors(cpe):
    # log sensor errors in logfile and console
    log_error('called process error: ' + str(cpe.cmd) + ' returned ' + str(cpe.returncode) + ': ' + cpe.output)


def treat_os_errors(ose):
    # log os errors in logfile and console
    log_error('oserror: ' + str(ose.strerror))


def treat_led_errors(cpe):
    # log led errors in logfile and console
    if cpe.returncode == 1:
        log_error('called process error: ' + str(cpe.cmd[0]) + ' returned 1: setup wiringPi failed')
    elif cpe.returncode == 2:
        log_error('called process error: ' + str(cpe.cmd[0]) + ' returned 2: invalid arguments')


def treat_requests_errors(re):
    # log requests errors in logfile and console and set status led color to orange
    log_error('requests failure: ' + str(re))
    set_status_led(LedStatusTypes.request_error.name)


def treat_sensor_broken_errors(sensortype):
    # log sensor broken errors in logfile and console and set status led color to red
    log_error(str(sensortype) + ' sensor broken')
    set_status_led(LedStatusTypes.sensor_broken.name)


def treat_missing_config_errors():
    log_error('No valid config file found! Please start config server!')


def treat_pairing_errors():
    log_error('No Token and/or UserId set in config file. Please pair your Raspberry Pi!')


# def check_credentials(token, userid):
#     logging.info('Start credentials check')
#     headers = {'Content-Type': 'application/json', 'Authorization': token}
#     try:
#         r = requests.get(API + CUSTOMERS + str(userid) + '/exists', headers=headers)
#     except requests.exceptions.RequestException, re:
#         # catch and treat requests errors
#         treat_requests_errors(re)
#     else:
#         return r.text


def set_status_led(status):
    command = ['sensors/rgb.out', str(status)]
    try:
        subproc = subprocess.check_call(command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
    except subprocess.CalledProcessError, cpe:
        # catch invalid arguments errors
        # catch wiringPi errors
        treat_led_errors(cpe)
    except OSError, ose:
        # catch os errors, e.g. file-not-found
        treat_os_errors(ose)
