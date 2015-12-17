'''
The database directory has this structure. ::

    ./current -> ./folders/Lists
    ./folders/INBOX/ # some-message-id
    ./folders/Lists/ # other-message-id
    ./folders/Sent/ # blah@blah.blah

'''
import os

class Current(object):

    def __init__(self, directory):
        os.makedirs(os.path.join(directory, 'folders'), exist_ok = True)
        self._directory = directory

    def __repr__(self):
        return 'Current(%s)' % repr(self._directory)

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

