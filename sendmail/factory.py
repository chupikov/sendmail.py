import os
import re


class MailProcessorFactory():
    package = "sendmail.processors."
    list = {}
    mods = {}

    def __init__(self, config):
        directory = os.path.dirname(os.path.realpath(__file__)) + "/processors"
        regex = re.compile("(.+Processor)\.py")
        print("Processors Directory: " + directory)
        l = os.listdir(directory)
        for line in l:
            m = regex.match(line)
            if m is None:
                continue
            name = m.group(1)
            pack = self.package + name
            print("> {} :: {} -- from {} import {}".format(line, name, pack, name))
            mod = __import__(pack, fromlist=[name])
            o = getattr(mod, name)
            self.mods[name] = o
        for conf in config:
            name = conf["name"]
            clazz = conf["class"]
            if not conf["enabled"]:
                continue
            print("Add: {}({})".format(name, clazz))
            self.list[name] = self.mods[clazz](conf)

    def get(self, name):
        try:
            if self.list[name]:
                return self.list[name]
            else:
                return None
        except Exception:
            return None

