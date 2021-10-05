#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import re


f = os.popen('tasklist /nh', 'r')
for eachLine in f:
    print(re.findall(r'([\w.]+(?: [\w.]+)*)\s\s+(\d+) \w+\s\s+\d+\s\s+([\d,]+ K)', eachLine.rstrip()))
f.close()