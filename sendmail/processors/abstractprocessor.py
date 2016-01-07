"""AbstractProcessor Sendmail module.

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

import abc
from email.message import Message


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.3"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class AbstractProcessor():
    """Abstract class that must be inherited by all message processors."""

    name = None

    def __init__(self, conf=None):
        """Creates new instance of processor and initializes it according to specified configuration.

        :param conf: Processor configuration
        :return: Instance of the processor class.
        """

        self.name = self.__class__.__name__
        for name in dir(self):
            value = getattr(self, name)
            if not callable(value):
                try:
                    configurable = False if name.index('__') == 0 else True
                except ValueError:
                    configurable = True
                if configurable:
                    try:
                        setattr(self, name, conf[name])
                        print("    {}.{} = '{}' ('{}')".format(self.__class__.__name__, name, conf[name], value))
                    except KeyError:
                        pass

    @abc.abstractmethod
    def process(self, message: Message):
        pass
