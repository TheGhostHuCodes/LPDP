from abc import ABCMeta, abstractmethod


class AbstractSubject(metaclass=ABCMeta):
    """A common interface for the real and proxy objects."""

    @abstractmethod
    def sort(self, reverse=False):
        pass
