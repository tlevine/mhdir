'''
The database maildir has this structure. ::

    ./current -> ./folders/Lists
    ./folders/INBOX/ # some-message-id
    ./folders/Lists/ # other-message-id
    ./folders/Sent/ # blah@blah.blah

'''
import os

class Current(object):

    def __init__(self, maildir):
        os.makedirs(maildir, exist_ok = True)
        self._maildir = maildir

    def __repr__(self):
        return 'Current(%s)' % repr(self._maildir)

    @property
    def _folder_path(self):
        return os.path.join(self._maildir, '.mhdir-current-folder')

    @property
    def folder(self):
        if os.path.islink(self._folder_path):
            return os.readlink(self._folder_path)

    @folder.setter
    def folder(self, src):
        if '/' in src:
            raise ValueError('Folder name may not contain a slash.')

        if os.path.isdir(os.path.join(self._maildir, src)):
            if os.path.islink(self._folder_path):
                os.unlink(self._folder_path)
            os.symlink(src, self._folder_path)
        else:
            raise NotADirectoryError(src)

    @property
    def _message_path(self):
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

c = Current('/Users/t/tom/maildir/hot/_@thomaslevine.com/')
print(c.folder)
# c.folder = '/Users/t/tom/maildir/hot/_@thomaslevine.com/INBOX'
c.folder = 'INBOX'
