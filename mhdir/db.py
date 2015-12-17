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
    def _folder_path(self):
        return os.path.join(self._directory, '.current')

    @property
    def folder(self):
        if os.path.islink(self._folder_path):
            return os.readlink(self._folder_path)

    @folder.setter
    def folder(self, dst):
        if '/' in dst:
            raise ValueError('Folder must not contain slashes.')
        if os.path.islink(self._folder_path):
            os.unlink(self._folder_path)
        os.symlink(os.path.join(self._directory, dst), self._folder_path)

    @property
    def _message_path(self):
        print(self._folder_path)
        return os.readlink(self._folder_path)

    @property
    def message(self):
        if os.path.islink(self._folder_path) and os.path.islink(self._message_path):
            return os.readlink(self._message_path)

    @message.setter
    def message(self, dst):
        if os.path.islink(self._message_path):
            os.unlink(self._message_path)
        os.symlink(dst, self._message_path)

c = Current('/tmp/blah')
