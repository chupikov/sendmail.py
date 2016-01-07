"""Sendmail application module.

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

from email import message_from_string
from sendmail.factory import MailProcessorFactory


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.3"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class Sendmail:
    """Sendmail application."""

    factory = None
    config = None

    def __init__(self, config=None):
        """Creates and configures application instance.

        :param config: Configuration array
        :return: Sendmail instance.
        """
        self.configure(config)

    def configure(self, config):
        """Configures application instance.

        :param config: Configuration array.
        :return: None
        """
        if config is None or self.factory is not None:
            return
        self.config = config
        self.factory = MailProcessorFactory(self.config)

    def execute(self, data: str):
        """Executes Sendmail application.

        :param data: E-Mail message as a plain text.
        """
        message = message_from_string(data)
        for name in self.factory.list:
            p = self.factory.get(name)
            if p is None:
                print("Processor not found: {}".format(name))
                continue

            print("Execute: {} ({})".format(name, p.__class__.__name__))
            p.process(message)
