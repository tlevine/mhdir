'''
The database directory has this structure. ::

    ./current -> ./folders/Lists
    ./folders/INBOX/ # some-message-id
    ./folders/Lists/ # other-message-id
    ./folders/Sent/ # blah@blah.blah

'''
import os

class SymlinkPointer(object):

    def __init__(self, directory):
        os.makedirs(directory, exist_ok = True)
        self._directory = directory

    def __repr__(self):
        return 'SymlinkMap(%s)' % repr(self._directory)

    @property
    def value(self):
        return os.readlink(os.path.join(self._directory, '.pointer'))

    @value.setter
    def value(self, dst):
        src = os.path.join(self._directory, '.pointer')
        os.symlink(src, dst)

class CurrentFolder(object):

    def __init__(self, file):
        self._file = file

    def __repr__(self):
        return 'Current(%s)' % repr(self._file)

    @property
    def folder(self):
        filename = os.path.join(self._directory, 'current')
        if os.path.isfile(filename):
            with open(filename) as fp:
                y = fp.read()
            return y.strip()

    @folder.setter
    def folder(self, x):
        filename = os.path.join(self._directory, 'current')
        with open(filename, 'w') as fp:
            fp.write(x)

