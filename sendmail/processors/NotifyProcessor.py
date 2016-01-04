import notify2
from sendmail.processors.abstractprocessor import AbstractProcessor


class NotifyProcessor(AbstractProcessor):
    title_template = "{appname}"
    text_template = "{subject}"
    icon_name = "mail-message-new"

    def __init__(self, conf=None):
        super(NotifyProcessor, self).__init__(conf)

    def process(self, message):
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
