#!/usr/bin/env python3
import abc
from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup


class AbstractFactory(metaclass=abc.ABCMeta):
    """Abstract factory interface provides 3 methods to implement in its subclasses: create_protocol, create_port, and create_parser."""

    def __init__(self, is_secure):
        """If is_secure is True, factory tries to make connection secure, otherwise not"""
        self.is_secure = is_secure

        @abc.abstractmethod
        def create_protocol(self):
            pass

        @abc.abstractmethod
        def create_port(self):
            pass

        @abc.abstractmethod
        def create_parser(self):
            pass


class HTTPFactory(AbstractFactory):
    """Concrete factory for building HTTP connection."""

    def create_protocol(self):
        return 'https' if self.is_secure else 'http'

    def create_port(self):
        return HTTPSecurePort() if self.is_secure else HTTPPort()

    def create_parser(self):
        return HTTPParser()


class FTPFactory(AbstractFactory):
    """Concrete factory for building FTP connection."""

    def create_protocol(self):
        return 'ftp'

    def create_port(self):
        return FTPPort()

    def create_parser(self):
        return FTPParser()


class Port(metaclass=abc.ABCMeta):
    """An abstract product, represents port to connect. One of its subclasses will be created in fatory methods."""

    @abc.abstractmethod
    def __str__(self):
        pass


class HTTPPort(Port):
    """A concrete product which represents http port."""

    def __str__(self):
        return '80'


class HTTPSecurePort(Port):
    """A concrete product which represents https port."""

    def __str__(self):
        return '443'


class FTPPort(Port):
    """A concrete product which represents ftp port."""

    def __str__(self):
        return '21'


class Parser(metaclass=abc.ABCMeta):
    """An abstract product, represents parser to parse web content. One of its subclasses will be created in factory methods."""

    @abc.abstractmethod
    def __call__(self, content):
        pass


class HTTPParser(Parser):
    def __call__(self, content):
        filenames = []
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.table.find('tbody').findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPParser(Parser):
    def __call__(self, content):
        lines = content.decode('utf-8').split('\n')
        filenames = []
        for line in lines:
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


class Connector():
    """A client."""

    def __init__(self, factory):
        """factory is a AbstractFactory instance which creates all attributes of a connector according to factory class."""
        self.protocol = factory.create_protocol()
        self.port = factory.create_port()
        self.parse = factory.create_parser()

    def read(self, host, path):
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print("Connecting to {}".format(url))
        return urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def parse(self):
        pass


if __name__ == '__main__':
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD/'

    protocol = int(
        input("Connecting to {}. Which Protocol to use? (0-http, 1-ftp): ".
              format(domain)))

    if protocol == 0:
        is_secure = bool(int(input("Use secure connection? (1-yes, 0-no): ")))
        factory = HTTPFactory(is_secure)
    elif protocol == 1:
        is_secure = False
        factory = FTPFactory(is_secure)
    else:
        print("Sorry, wrong answer")

    connector = Connector(factory)
    try:
        content = connector.read(domain, path)
    except URLError as e:
        print("Can not access resource with this method")
    else:
        print(connector.parse(content))
