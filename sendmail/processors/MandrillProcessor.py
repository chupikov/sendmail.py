"""Sendmail MandrillProcessor module.

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

from mandrill.mandrill import Mandrill, Error
from email.message import Message
from sendmail.processors.abstractprocessor import AbstractProcessor


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.5"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class MandrillProcessor(AbstractProcessor):
    """Sends messages using Mandrill API."""

    apikey = None
    to_address = None
    from_address = None
    from_name = "Sendmail.py"

    def __init__(self, conf=None):
        """Creates new instance and initializes it according to specified configuration.

        :param conf: Processor configuration.
        :return: New processor instance.
        """

        super(MandrillProcessor, self).__init__(conf)

    def process(self, message: Message):
        """Sends specified message via Mandrill API.

        :param message: Message to send.
        """

        print("  - {}: {}.process()".format(self.name, self.__class__.__name__))

        if not self.apikey:
            print("  - {}: {}.process(): Mandrill API key not specified.".format(self.name, self.__class__.__name__))
            return

        client = Mandrill(self.apikey)

        content = self.extractContent(message)

        msg = {
            'html': content,
            'subject': message.get("Subject"),
            'from_email': self.from_address,
            'from_name': self.from_name,
            'to': [
                {
                    "email": self.to_address
                },
            ],
        }

        try:
            result = client.messages.send(message=msg)
            i = 0
            for item in result:
                i += 1
                print("  - {}: {}.process(): {}. {} -- {}".format(
                    self.name,
                    self.__class__.__name__,
                    str(i),
                    item["email"],
                    item["status"]))
        except Error as e:
            print("  - {}: {}.process(): ERROR: {} - {}".format(
                self.name,
                self.__class__.__name__,
                e.__class__,
                e
            ))
