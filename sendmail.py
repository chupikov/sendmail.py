#!/usr/bin/env python3

"""Configure and runs Sendmail application.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os
import sys
import json
import argparse
from sendmail.sendmail import Sendmail


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.3"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


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
