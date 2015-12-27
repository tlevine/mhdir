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
        self._maildir.mkdir(parents = True)
        
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
    def message(self, id_or_path):
        if id_or_path in self.messageid_path:
            id_or_path = Path(self.messageid_path[id_or_path])
        if id_or_path.parent.name not in {'new', 'cur', 'tmp'} or \
            id_or_path.parent.parent.parent != self._maildir:
            raise ValueError('Message must be inside the maildir %s.' % self._maildir)

        p = Path(id_or_path)
        target = str(p.relative_to(p.parent.parent))
        print(target)
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
