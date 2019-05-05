#!/usr/bin/env python
# -*- coding: utf-8 -*

import subprocess
import time
import datetime


while True:
    order = 'adb shell free -m'

    pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)

    for line in iter(pi.stdout.readline, 'b'):
        line = line.decode('utf-8')
        line = line.strip('\n')
        line = line.strip('\r')
        if line:
            print(line)
