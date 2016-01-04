from email import message_from_string
from sendmail.factory import MailProcessorFactory


class Sendmail():
    factory = None
    config = None

    def __init__(self, config=None):
        self.configure(config)

    def configure(self, config):
        if config is None or self.factory is not None:
            return
        self.config = config
        self.factory = MailProcessorFactory(self.config)

    def execute(self, data):
        message = message_from_string(data)
        for name in self.factory.list:
            p = self.factory.get(name)
            if p is None:
                print("Processor not found: {}".format(name))
                continue

            print("Execute: {} ({})".format(name, p.__class__.__name__))
            p.process(message)
