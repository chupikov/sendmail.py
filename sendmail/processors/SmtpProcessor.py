import smtplib
from sendmail.processors.abstractprocessor import AbstractProcessor


class SmtpProcessor(AbstractProcessor):
    username = None
    password = None
    host = None
    port = 25
    from_address = None
    to_address = None
    starttls = True

    def __init__(self, conf=None):
        super(SmtpProcessor, self).__init__(conf)

    def process(self, message):
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
