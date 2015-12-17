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
        os.makedirs(directory, exist_ok = True)
        self._directory = directory

    def __repr__(self):
        return 'Current(%s)' % repr(self._directory)

    @property
    def _current_path(self):
        return os.path.join(self._directory, '.current')

    @property
    def folder(self):
        if os.path.islink(self._current_path):
            return os.readlink(self._current_path)

    @folder.setter
    def folder(self, dst):
        if os.path.islink(self._current_path):
            os.unlink(self._current_path)
        os.symlink(dst, self._current_path)

    @property
    def message(self):
        if os.path.islink(self._current_path):
            with open(self._current_path) as fp:
                path = fp.read()
            return path.strip()

    @message.setter
    def message(self, x):
        with open(self._current_path, 'w') as fp:
            fp.write(x)

abc =  Current('/tmp/abc')
print(abc.folder)
