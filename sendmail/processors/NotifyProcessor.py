"""Sendmail NotifyProcessor module.

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


import notify2
from email.message import Message
from sendmail.processors.abstractprocessor import AbstractProcessor


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.3"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class NotifyProcessor(AbstractProcessor):
    """Displays desktop notification messages."""

    title_template = "{appname}"
    text_template = "{subject}"
    icon_name = "mail-message-new"

    def __init__(self, conf=None):
        """Creates new instance and initializes it according to specified configuration.

        :param conf: Processor configuration.
        :return: New processor instance.
        """

        super(NotifyProcessor, self).__init__(conf)

    def process(self, message: Message):
        """Displays desktop notification about specified message.

        :param message: E-Mail message object.
        """

        print("  - {}: {}.process()".format(self.name, self.__class__.__name__))

        notify2.init("Sendmail")

        title = self.title_template.format(
            subject=message.get("Subject"),
            from_email=message.get("From"),
            appname="Sendmail",
            name=self.name
        )
        text = self.text_template.format(
            subject=message.get("Subject"),
            from_email=message.get("From"),
            text=message.as_string(),
            appname="Sendmail",
            name=self.name
        )

        n = notify2.Notification(title,
            text,
            self.icon_name
        )

        n.show()
