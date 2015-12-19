'''
The database maildir has this structure. ::

    ./current -> ./folders/Lists
    ./folders/INBOX/ -> /some/message
    ./folders/Lists/ -> /other/message
    ./folders/Sent/ -> /blah/blah

'''
import os
from pathlib import Path
import re
import csv

class MHDir(object):
    # TODO: Store this as formal IMAP messages so they sync
    def __init__(self, maildir):
        self._maildir = maildir
        self._maildir.mkdir(exist_ok = True)
        
        self.messageid_path = CSVMap(maildir / '.mhdir-messageid-path')
        self.path_messageid = CSVMap(maildir / '.mhdir-path-messageid')

    def __repr__(self):
        return 'Current(%s)' % repr(self._maildir)

    @property
    def _folder_path(self):
        return self._maildir / '.mhdir-current-folder'

    @property
    def folder(self):
        if self._folder_path.is_symlink():
            return self._folder_path.resolve()

    @folder.setter
    def folder(self, target):
        if '/' in target:
            raise ValueError('Folder name may not contain a slash.')

        # Set current folder.
        if (self._maildir / target).is_dir():
            if self._folder_path.is_symlink():
                self._folder_path.unlink()
            self._folder_path.symlink_to(target)
        else:
            raise NotADirectoryError(target)

        # Set current message
        if self.message == None:
            messages = self.folder.glob('cur/*')
            try:
                self.message = next(messages)
            except StopIteration:
                pass

    @property
    def _message_path(self):
        if not self._folder_path.is_symlink():
            raise ValueError('Set the current folder first.')
        return self._maildir / os.readlink(str(self._folder_path)) / '.mhdir-current-message'

    @property
    def message(self):
        if self._message_path.is_symlink():
            return self._message_path.resolve()

    @message.setter
    def message(self, target):
        if target in self.messageid_path:
            target = str(Path(target).relative_to(self._maildir))

        if target[:4] not in {'new/', 'cur/', 'tmp/'}:
            raise ValueError('Message path must start with "new/", "cur/", or "tmp/".')
        if '/' in target[4:]:
            raise ValueError('Aside from the fourth character, the message path must contain no slashes.')

        if self._message_path.is_symlink():
            self._message_path.unlink()
        self._message_path.symlink_to(target)

def folder_messages(folder: Path):
    for sub in folder.iterdir():
        if sub.name in ['new', 'cur', 'tmp']:
            for subsub in sub.iterdir():
                if re.match(r'^[0-9]', subsub.name):
                    yield subsub

def prev_cur_next(current_message):
    base = current_message.parent.name, current_message.name.split(':')[0]
    results = {}
    for message in folder_messages(current_message.parent.parent):
        this = message.parent.name, message.name.split(':')[0]
        if this < base:
            results['prev'] = message
        elif this == base:
            results['show'] = message
        elif this > base:
            results['next'] = message
            break
    return results

class CSVMap(dict):
    def __init__(self, file):
        super(CSVMap, self).__init__()
        if file.exists():
            fp = file.open('a+')
            fp.seek(0)
            self.update(dict(csv.reader(fp)))
        else:
            fp = file.open('a+')
        self._writer = csv.writer(fp)

    def __setitem__(self, key, value):
        self._writer.writerow((key, value))
        super(CSVMap, self).__setitem__(key, value)

if __name__ == '__main__':
    c = Current(Path('/Users/t/tom/maildir/hot/_@thomaslevine.com/'))
    print(c.folder)
    # c.folder = '/Users/t/tom/maildir/hot/_@thomaslevine.com/INBOX'
    c.folder = 'INBOX'
    c.message = 'cur/1440863938_0.9286._,U=98351,FMD5=7e33429f656f1e6e9d79b29c3f82c57e:2,S'
    print(prev_cur_next(c.message))
