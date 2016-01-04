#!/usr/bin/env python3

import os
import sys
import notify2
import pyinotify
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Directory for watching.")
args = parser.parse_args()
if args.dir:
    dirname = args.dir
else:
    sys.stderr.write("ERROR! Directory not specified.\n")
    sys.exit(1)

if not os.path.isdir(dirname):
    sys.stderr.write("ERROR! Directory not found: {}\n".format(dirname))
    sys.exit(1)


notify2.init("Sendmail Watcher")

wm = pyinotify.WatchManager()

mask = pyinotify.IN_CREATE


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating: ", event.pathname)
        n = notify2.Notification('Sendmail File Created',
                'New message: {}'.format(event.pathname),
                'mail-message-new'
        )
        n.show()

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(dirname, mask, rec=True)

notifier.loop()
