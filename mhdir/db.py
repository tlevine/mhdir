'''
The database maildir has this structure. ::

    ./current -> ./folders/Lists
    ./folders/INBOX/ # some-message-id
    ./folders/Lists/ # other-message-id
    ./folders/Sent/ # blah@blah.blah

'''
import os
from pathlib import Path

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
        if not os.path.islink(self._folder_path):
            raise ValueError('Set the current folder first.')
        return os.path.join(self._maildir, os.readlink(self._folder_path), '.mhdir-current-message')

    @property
    def message(self):
        if os.path.islink(self._message_path):
            return os.readlink(self._message_path)

    @message.setter
    def message(self, src):
        if src[:4] not in {'new/', 'cur/', 'tmp/'}:
            raise ValueError('Message path must start with "new/", "cur/", or "tmp/".')
        if '/' in src[4:]:
            raise ValueError('Aside from the fourth character, the message path must contain no slashes.')

        if os.path.islink(self._message_path):
            os.unlink(self._message_path)
        os.symlink(src, self._message_path)

c = Current('/Users/t/tom/maildir/hot/_@thomaslevine.com/')
print(c.folder)
# c.folder = '/Users/t/tom/maildir/hot/_@thomaslevine.com/INBOX'
c.folder = 'INBOX'
c.message = 'cur/1440863938_0.9286._,U=98351,FMD5=7e33429f656f1e6e9d79b29c3f82c57e:2,S'

def folder_messages(folder: Path):
    for sub in folder.iterdir():
        if sub.name in ['new', 'cur', 'tmp']:
            for subsub in sub.iterdir():
                if re.match(r'^[0-9]', subsub.name):
                    yield subsub
