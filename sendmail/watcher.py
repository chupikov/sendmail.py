import os
import sys
import json
import signal
import notify2
import argparse
import pyinotify
import subprocess
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from multiprocessing import Process


class FilesystemWatcher():
    directories = []
    name = 'Sendmail Watcher'
    notification_icon = 'mail-message-new'
    appindicator_icon = 'envelop-white.svg'
    config_file = None
    watch_manager = None
    notifier = None
    notifier_loop_process = None
    watchers = []

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dir', help='Directory for watching.')
        parser.add_argument('-c', '--config', help='Config file name.')
        parser.add_argument('--appicon', help='System tray icon filename. File should be located in the "icons" directory.')
        parser.add_argument('--notifyicon', help='Notification popup message icon name. Default "mail-message-new".')
        args = parser.parse_args()

        if args.appicon:
            self.appindicator_icon = args.appicon

        if args.notifyicon:
            self.notification_icon = args.notifyicon

        if args.config:
            filename = args.config
            self.load_config(filename)

        if args.dir:
            print("Add: {}({})".format('--dir', args.dir))
            self.directories.append(args.dir)

        if len(self.directories) == 0:
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

    def load_config(self, filename):
        print('Load config "{}"...'.format(filename))
        f = open(filename, encoding="UTF-8")
        config = json.loads(f.read())
        f.close()
        for conf in config:
            if conf['class'] == 'FilesystemProcessor' and conf['enabled']:
                print("Add: {}({})".format(conf['name'], conf['directory']))
                self.directories.append(conf['directory'])

    def build_menu(self):
        menu = gtk.Menu()
        for dir in self.directories:
            item = gtk.MenuItem(os.path.abspath(dir))
            item.connect('activate', self.open_directory)
            menu.append(item)
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.application_quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def open_directory(self, source):
        print('Open dir: {}'.format(source.get_label()))
        subprocess.call(['exo-open', '--launch', 'FileManager', source.get_label()])

    def application_quit(self, source):
        self.notifier_loop_process.terminate()
        sys.exit(0)

    def execute(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        icon = os.path.abspath('icons/{}'.format(self.appindicator_icon))
        indicator = appindicator.Indicator.new('FilesystemWatcherIndicator', icon, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())

        self.notifier_loop_process = Process(target=self.notifier.loop)
        self.notifier_loop_process.start()

        gtk.main()


class FilesystemEventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print('Created: ', event.pathname)
        n = notify2.Notification('Sendmail File Created',
                'New message: {}'.format(event.pathname),
                'mail-message-new'
        )
        n.show()
