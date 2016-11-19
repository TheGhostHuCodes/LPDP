#!/usr/bin/env python3
class SimpleFactory():
    @staticmethod
    def build_connection(protocol):
        if protocol == 'http':
            return HTTPConnection()
        elif protocol == 'ftp':
            return FTPConnection()
        else:
            raise RuntimeError("Unknown protocol")


class HTTPConnection():
    def __init__(self):
        print("running {} constructor".format(self.__class__))

    def connect(self):
        print("connecting with {}".format(self.__class__))

    def get_response(self):
        return "response received using {}".format(self.__class__)


class FTPConnection():
    def __init__(self):
        print("running {} constructor".format(self.__class__))

    def connect(self):
        print("connecting with {}".format(self.__class__))

    def get_response(self):
        return "response received using {}".format(self.__class__)


if __name__ == '__main__':
    protocol = input("Which Protocol to use? (http or ftp): ")
    protocol = SimpleFactory.build_connection(protocol)
    protocol.connect()
    print(protocol.get_response())
