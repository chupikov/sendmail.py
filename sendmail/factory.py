"""MailProcessorFactory module.

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
import re
from sendmail.processors.abstractprocessor import AbstractProcessor


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.4"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class MailProcessorFactory:
    """Contains list of processors as classes and returns processors by names defined in the configuration file."""

    package = "sendmail.processors."
    list = {}
    mods = {}

    def __init__(self, config):
        """Loads list of available processor classes and creates list of AbstractProcessor instances for each definition in the config file.

        :param config: Application configuration array.
        """

        directory = os.path.dirname(os.path.realpath(__file__)) + "/processors"
        regex = re.compile("(.+Processor)\.py")
        print("Processors Directory: " + directory)
        for conf in config:
            name = conf["name"]
            clazz = conf["class"]
            if not conf["enabled"]:
                continue
            moduleExists = False
            try:
                if self.mods[clazz]:
                    moduleExists = True
            except:
                pass
            if not moduleExists:
                pack = self.package + clazz
                print("> {} -- from {} import {}".format(clazz, pack, clazz))
                mod = __import__(pack, fromlist=[clazz])
                o = getattr(mod, clazz)
                self.mods[clazz] = o
            print("Add: {}({})".format(name, clazz))
            self.list[name] = self.mods[clazz](conf)

    def get(self, name: str) -> AbstractProcessor:
        """Returns Processor instance according to name.

        :param name: Name of the processor as it defined in the configuration file, for example 'Test FileSystem'.
        :return: Processor instance assigned to specified name; None if specified name not found.
        """
        try:
            if self.list[name]:
                return self.list[name]
            else:
                return None
        except Exception:
            return None
