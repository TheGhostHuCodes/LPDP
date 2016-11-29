from abc import ABCMeta, abstractmethod
import os

history = []


class Command(metaclass=ABCMeta):
    """The command interface."""

    @abstractmethod
    def execute(self):
        """Method to execute the command."""
        pass

    @abstractmethod
    def undo(self):
        """A method to undo the command."""
        pass


class LsCommand(Command):
    """Concrete command that emulates ls unix command behavior."""

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        """The command delegates the call to its receiver."""
        self.receiver.show_current_dir()

    def undo(self):
        """Can not undo ls command."""
        pass


class LsReceiver:
    def show_current_dir(self):
        """The receiver knows how to execute the command."""
        cur_dir = './'
        filenames = []
        for filename in os.listdir(cur_dir):
            if os.path.isfile(os.path.join(cur_dir, filename)):
                filenames.append(filename)

        print("Content of dir: ", ' '.join(filenames))


class TouchCommand(Command):
    """Concrete command that emulates touch unix command behavior."""

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.create_file()

    def undo(self):
        self.receiver.delete_file()


class TouchReceiver:
    def __init__(self, filename):
        self.filename = filename

    def create_file(self):
        """Actual implementation of unix touch command."""
        with open(self.filename, 'a'):
            os.utime(self.filename, None)

    def delete_file(self):
        """Undo unix touch command. Here we simply delete the file."""
        os.remove(self.filename)


class RmCommand(Command):
    """Concrete command that emulates rm unix command behavior."""

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.delete_file()

    def undo(self):
        self.receiver.undo()


class RmReceiver:
    def __init__(self, filename):
        self.filename = filename
        self.backup_name = None

    def delete_file(self):
        """Deletes file with creating backup to store it in undo method."""
        self.backup_name = '.' + self.filename
        os.rename(self.filename, self.backup_name)

    def undo(self):
        """Restores the deleted file."""
        original_name = self.backup_name[1:]
        os.rename(self.backup_name, original_name)
        self.backup_name = None
