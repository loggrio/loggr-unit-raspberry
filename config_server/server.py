from flask import Flask, request, jsonify
from os import path
import re
import logging
from ConfigParser import ConfigParser
from flask.ext.cors import CORS
from raspi_loggr.util import set_status_led
from raspi_loggr.util import log_info
from raspi_loggr.util import log_error
from raspi_loggr.util import LedStatusTypes
server = Flask(__name__)
config = ConfigParser()

HOME_DIR = path.expanduser("~")
CONFIG_FILE = HOME_DIR + '/.loggrrc'

CORS(server, methods=['POST'], allow_headers='Content-Type')


@server.route('/', methods=['POST'])
def save_token_and_userid():
    config.read(CONFIG_FILE)

    regex_userid = re.compile(r'^[a-z,0-9]{24}$')
    regex_token = re.compile(r'^[A-Z,a-z,0-9]{64}$')

    if 'token' not in request.json and 'userid' not in request.json:
        log_error('missing arguments in post request')
        return jsonify(error='arguments')

    if 'token' in request.json:
        if regex_token.match(request.json['token']) is None:
            log_error('wrong format of token string')
            return jsonify(error='format')
        config.set('AUTH', 'token', request.json['token'])
        log_info('token set in config file')

    if 'userid' in request.json:
        if regex_userid.match(request.json['userid']) is None:
            log_error('wrong format of userid string')
            return jsonify(error='format')
        config.set('AUTH', 'userid', request.json['userid'])
        log_info('userid set in config file')

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    set_status_led(LedStatusTypes.pairing_succeeded.name)
    return jsonify(status='ok')


def init_config():
    # If config file not exists create a default one
    if not path.isfile(CONFIG_FILE):
        log_info('No config file found, create default one')
        config.add_section('AUTH')
        config.add_section('SENSORS')
        config.set('AUTH', 'token', '')
        config.set('AUTH', 'userid', '')
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        log_info('Created default config file')
        return

    config.read(CONFIG_FILE)

    if not config.has_section('AUTH'):
        config.add_section('AUTH')

    if not config.has_section('SENSORS'):
        config.add_section('SENSORS')

    if not config.has_option('AUTH', 'token'):
        config.set('AUTH', 'token', '')

    if not config.has_option('AUTH', 'userid'):
        config.set('AUTH', 'userid', '')

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def main():
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', filename='server.log', level=logging.INFO)
    init_config()
    server.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    main()
