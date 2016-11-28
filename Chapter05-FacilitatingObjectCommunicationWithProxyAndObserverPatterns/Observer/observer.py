from abc import ABCMeta, abstractmethod
import datetime


class Observer(metaclass=ABCMeta):
    """Abstract class for observers, provides notify method as
    interface for subjects."""

    @abstractmethod
    def notify(self, unix_timestamp):
        pass


class USATimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime(
            '%Y-%m-%d %I:%M:%Sp')
        print("Observer {} says: {}".format(self.name, time))


class EUTimeObserver(Observer):
    def __init__(self, name):
        self.name = name

    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime(
            '%Y-%m-%d %H:%M:%S')
        print("Observer {} says: {}".format(self.name, time))
