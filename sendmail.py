#!/usr/bin/env python3

import os
import sys
import json

from sendmail.sendmail import Sendmail

# filename = os.getcwd() + "/config.json"
filename = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
f = open(filename, encoding="UTF-8")
sendmail = Sendmail(json.loads(f.read()))
f.close()
sendmail.execute(sys.stdin.read())
