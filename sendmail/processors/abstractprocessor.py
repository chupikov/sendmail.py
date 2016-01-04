import abc


class AbstractProcessor():
    name = None

    def __init__(self, conf=None):
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
    def process(self, message):
        pass
