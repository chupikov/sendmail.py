import os
import sys
import notify2
import pyinotify
import argparse
import signal
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

    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.application_quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

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
        print('Creating: ', event.pathname)
        n = notify2.Notification('Sendmail File Created',
                'New message: {}'.format(event.pathname),
                'mail-message-new'
        )
        n.show()
