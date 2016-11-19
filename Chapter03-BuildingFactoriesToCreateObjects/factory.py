#!/usr/bin/env python3
import abc
from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Connector(metaclass=abc.ABCMeta):
    """Abstract class to connect to remote resource."""

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self):
        """Parses web content.
        This method should be redefined in the runtime."""
        pass

    def read(self, host, path):
        """A generic method for all subclasses, reads web content."""
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print("Connecting to {}".format(url))
        return urlopen(url, timeout=2).read()

    @abc.abstractmethod
    def protocol_factory_method(self):
        """A factory method that must be redefined in subclass."""
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        """A factory method that must be redefined in subclass."""
        pass


class HTTPConnector(Connector):
    """A concerete creator that creates a HTTP connector and sets in runtime all its attributes."""

    def protocol_factory_method(self):
        return 'https' if self.is_secure else 'http'

    def port_factory_method(self):
        """Here HTTPPort and HTTPSecurePort are concrete objects, craeted by factory method."""
        return HTTPSecurePort() if self.is_secure else HTTPPort()

    def parse(self, content):
        """Parses web content."""
        filenames = []
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.table.find('tbody').findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPConnector(Connector):
    """A concerete creator that creates a FTP connector and sets in runtime all its attributes."""

    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return FTPPort()

    def parse(self, content):
        lines = content.decode('utf-8').split('\n')
        filenames = []
        for line in lines:
            # The FTP format typically has 8 columns, split them
            splitted_line = line.split(None, 8)
            if len(splitted_line) == 9:
                filenames.append(splitted_line[-1])
        return '\n'.join(filenames)


class Port(metaclass=abc.ABCMeta):
    """Abstract product. One of its subclasses will be created in factory methods."""

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


if __name__ == '__main__':
    domain = 'ftp.freebsd.org'
    path = '/pub/FreeBSD/'

    protocol = int(
        input("Connecting to {}. Which Protocol to use? (0-http, 1-ftp): ".
              format(domain)))

    if protocol == 0:
        is_secure = bool(int(input("Use secure connection? (1-yes, 0-no): ")))
        connector = HTTPConnector(is_secure)
    else:
        is_secure = False
        connector = FTPConnector(is_secure)

    try:
        content = connector.read(domain, path)
    except URLError as e:
        print("Can not access resource with this method")
    else:
        print(connector.parse(content))
