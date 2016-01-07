"""Sendmail FilesystemProcessor module.

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
from email.message import Message
from sendmail.processors.abstractprocessor import AbstractProcessor


__author__ = "Yaroslav Chupikov"
__copyright__ = "Copyright 2016, Celtic Logic Limited"
__license__ = "GPL"
__version__ = "0.3"
__email__ = "yaroslav@mirasoltek.com"
__status__ = "Production"


class FilesystemProcessor(AbstractProcessor):
    """Stores messages as files."""

    directory = '/var/mail/sendmail/new'
    num_file = '/var/mail/sendmail/num'
    extension = '.txt'
    number = 0
    name_length = 4

    def __init__(self, conf=None):
        """Creates new instance and initializes it according to specified configuration.

        :param conf: Processor configuration.
        :return: New processor instance.
        """

        super(FilesystemProcessor, self).__init__(conf)

    def init_filesystem(self):
        """Loads next message number from file or creates required directories."""

        if not os.path.isdir(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        if os.path.isfile(self.num_file):
            f = open(self.num_file, mode="r", encoding="utf-8")
            self.number = int(f.readline())
            f.close()
        else:
            f = open(self.num_file, mode="w", encoding="utf-8")
            f.write(str(self.number))
            f.close()

    def increase_number(self):
        """Increases message number and saves it in the file for next usage."""

        self.number += 1
        f = open(self.num_file, "w")
        f.write(str(self.number))
        f.close()

    def process(self, message: Message):
        """Saves specified message in the file.

        :param message: Message to save.
        """

        print("  - {}: {}.process()".format(self.name, self.__class__.__name__))
        self.init_filesystem()
        filename = "{}/{}{}".format(self.directory, str(self.number).zfill(self.name_length), self.extension)
        print("  - {}: from: {}".format(self.name, message.get("From")))
        print("  - {}: subject: {}".format(self.name, message.get("Subject")))
        print("  - {}: content type: {}".format(self.name, message.get_content_type()))
        print("  - {}: filename: {}".format(self.name, filename))
        f = open(filename, "w")
        f.write(message.as_string())
        f.close()
        self.increase_number()
