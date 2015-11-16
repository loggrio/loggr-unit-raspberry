#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import *
from time import sleep, strftime
from datetime import datetime
import time

cmd_show = "DISPLAY=:0.0 vlc -vvv -f http://141.60.125.254:8080/?action=stream 2>&1 > /tmp/vlc.log"

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

ret = run_cmd(cmd_show)
