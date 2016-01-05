import os
import sys
import notify2
import pyinotify
import argparse


class FilesystemWatcher():
    directories = []
    name = 'Sendmail Watcher'
    icon = 'mail-message-new'
    config_file = None
    watch_manager = None
    notifier = None
    watchers = []

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dir', help='Directory for watching.')
        parser.add_argument('-c', '--config', help='Config file name.')
        args = parser.parse_args()

        if args.dir:
            self.directories.append(args.dir)
        else:
            sys.stderr.write("ERROR! Directory not specified.\n")
            sys.exit(1)

        notify2.init(self.name)
        self.watch_manager = pyinotify.WatchManager()
        handler = FilesystemEventHandler()
        self.notifier = pyinotify.Notifier(self.watch_manager, handler)

        for directory in self.directories:
            if not os.path.isdir(directory):
                sys.stderr.write("ERROR! Directory not found: {}\n".format(directory))
                sys.exit(1)
            self.watchers.append(self.watch_manager.add_watch(directory, pyinotify.IN_CREATE, rec=True))

    def execute(self):
        self.notifier.loop()


class FilesystemEventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print('Creating: ', event.pathname)
        n = notify2.Notification('Sendmail File Created',
                'New message: {}'.format(event.pathname),
                'mail-message-new'
        )
        n.show()
