#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import imp
import logging
import requests
from os import path
from enum import Enum
from .sensor import Sensor
from ConfigParser import ConfigParser
from .util import set_status_led
from .util import LedStatusTypes
from .util import SensorTypes
from .util import treat_requests_errors
from .util import treat_missing_config_errors
from .util import treat_pairing_errors
from .util import log_info

TIME_BETWEEN_METERINGS = 60
TIME_BETWEEN_API_TESTS = 60

API = 'http://0.0.0.0:3000/api/'
CUSTOMERS = 'Customers/'
EXISTS = '/exists'

HOME_DIR = path.expanduser("~")
CONFIG_FILE = HOME_DIR + '/.loggrrc'


def main():
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', filename='loggr.log', level=logging.INFO)
    logging.info('Logging (re)started')

    # Check if config file exists
    if not path.isfile(CONFIG_FILE):
        treat_missing_config_errors()
        return

    # Create config
    config = ConfigParser()
    # Read config file
    config.read(CONFIG_FILE)

    # Check if config file contains options token and userid
    if not config.has_option('AUTH', 'token') or not config.has_option('AUTH', 'userid'):
        treat_missing_config_errors()
        return

    # Get token and user id from config file
    token = config.get('AUTH', 'token')
    userid = config.get('AUTH', 'userid')

    # Check if token and userid is set
    if not len(token) or not len(userid):
        treat_pairing_errors()
        return

    headers = {'Content-Type': 'application/json', 'Authorization': token}
    api_offline = True
    while api_offline:
        try:
            requests.get(API + CUSTOMERS + userid + EXISTS, headers=headers)
            api_offline = False
        except requests.exceptions.RequestException, re:
            treat_requests_errors(re)
            log_info('Api not reachable. Try again in ' + str(TIME_BETWEEN_API_TESTS) + ' seconds.')
            api_offline = True
            time.sleep(TIME_BETWEEN_API_TESTS)

    sensors = {}

    # Get list of options from config file (section: SENSORS)
    sensor_configs = config.options('SENSORS')

    # Iterate through sensor configs from config file
    for sensor in sensor_configs:
        # Get script name, location and unit from config file
        script, location, unit = config.get('SENSORS', sensor).split(',')
        # Get script suffix
        script_suffix = script.split('.')[1]

        if script_suffix == 'py':
            # Path to metering script
            p = 'sensors/' + script
            # Get function reference and import module generically
            func = imp.load_source('meter', p)
            # Create sensor generically and save it into a dictionary
            sensors[sensor] = Sensor(sensor, location, unit, func=func.meter)
        else:
            # Create sensor generically and save it into a dictionary
            sensors[sensor] = Sensor(sensor, location, unit, script=script)

    while True:
        # Iterate through sensor config values
        for s in sensors.itervalues():
            # Start metering and sending
            ret = s.meter_and_send()
            if ret == 200:
                set_status_led(LedStatusTypes.ok.name)

        time.sleep(TIME_BETWEEN_METERINGS)
