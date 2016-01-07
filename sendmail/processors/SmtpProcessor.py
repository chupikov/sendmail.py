"""Sendmail SmtpProcessor module.

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


import smtplib
from email.message import Message
from sendmail.processors.abstractprocessor import AbstractProcessor


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.3"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class SmtpProcessor(AbstractProcessor):
    """Sends messages using SMTP server."""

    username = None
    password = None
    host = None
    port = 25
    from_address = None
    to_address = None
    starttls = True

    def __init__(self, conf=None):
        """Creates new instance and initializes it according to specified configuration.

        :param conf: Processor configuration.
        :return: New processor instance.
        """

        super(SmtpProcessor, self).__init__(conf)

    def process(self, message):
        """Sends specified message via SMTP server.

        :param message: Message to send.
        """

        print("  - {}: {}.process()".format(self.name, self.__class__.__name__))

        if not self.from_address:
            self.from_address = self.username

        print("  - {}: from: {}".format(self.name, message.get("From")))
        print("  - {}: subject: {}".format(self.name, message.get("Subject")))
        print("  - {}: content type: {}".format(self.name, message.get_content_type()))

        with smtplib.SMTP(self.host, self.port) as server:
            print('  - Enable secure connection...')
            if self.starttls:
                server.starttls()
            print('  - Log in as "' + self.username + '"...')
            server.login(self.username, self.password)
            print('  - Start sending E-Mail message...')
            server.sendmail(from_addr=self.username, to_addrs=self.to_address, msg=message.as_string())
            print('  - Quit server...')
            server.quit()
