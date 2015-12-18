import os
from pathlib import Path

from . import parse
from .db import CSVMap

MAILDIR = Path('/Users/t/tom/maildir/hot/_@thomaslevine.com/')

def inc():
    '''
    1. If the message-id lookup doesn't exist, read everything in "cur" and add to the message-id lookup cache.
    2. Read everything in "new", add it to the message-id cache, and move it to "cur".
    '''
    messageid_path = CSVMap(os.path.expanduser('~/.mhdir-messageid-path'))
    path_messageid = CSVMap(os.path.expanduser('~/.mhdir-path-messageid'))
    for folder in MAILDIR.iterdir():
        for mail in (folder / 'cur').iterdir():
            if str(mail) not in path_messageid:
                with mail.open('rb') as fp:
                    message_id = parse.message_id(fp)
                messageid_path[message_id] = str(mail)
                path_messageid[str(mail)] = message_id

if __name__ == '__main__':
    inc()
