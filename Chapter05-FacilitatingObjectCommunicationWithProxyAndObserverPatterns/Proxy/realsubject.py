from abstractsubject import AbstractSubject
import random


class RealSubject(AbstractSubject):
    """A class for a heavy object which takes a lot of memory space and takes
    some time to instantiate."""

    def __init__(self):
        self.digits = []

        for i in range(10000000):
            self.digits.append(random.random())

    def sort(self, reverse=False):
        self.digits.sort()

        if reverse:
            self.digits.reverse()
