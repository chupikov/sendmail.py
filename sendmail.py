#!/usr/bin/env python3

import os
import sys
import json
import argparse
from sendmail.sendmail import Sendmail

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Config file name.")
args = parser.parse_args()
if args.config:
    filename = args.config
else:
    if os.path.isfile(os.getcwd() + '/sendmail.json'):
        filename = os.getcwd() + '/sendmail.json'
    else:
        filename = os.path.dirname(os.path.realpath(__file__)) + "/config.json"

if not os.path.isfile(filename):
    sys.stderr.write("ERROR! Config file not found: {}\n".format(filename))
    sys.exit(1)

f = open(filename, encoding="UTF-8")
sendmail = Sendmail(json.loads(f.read()))
f.close()
sendmail.execute(sys.stdin.read())
