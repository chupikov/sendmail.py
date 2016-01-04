import os
from sendmail.processors.abstractprocessor import AbstractProcessor


class FilesystemProcessor(AbstractProcessor):
    directory = '/var/mail/sendmail/new'
    num_file = '/var/mail/sendmail/num'
    extension = '.txt'
    number = 0
    name_length = 4

    def __init__(self, conf=None):
        super(FilesystemProcessor, self).__init__(conf)

    def init_filesystem(self):
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
        self.number += 1
        f = open(self.num_file, "w")
        f.write(str(self.number))
        f.close()

    def process(self, message):
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
