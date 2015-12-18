import os
from pathlib import Path

from . import parse
from .db import CSVMap

MAILDIR = Path('/Users/t/tom/maildir/hot/_@thomaslevine.com/')


PASSED = 'P' # the user has resent/forwarded/bounced this message to someone else.
REPLIED = 'R' # the user has replied to this message.
SEEN = 'S' # the user has viewed this message, though perhaps he didn't read all the way through it.
TRASHED = 'T' # the user has moved this message to the trash; the trash will be emptied by a later user action.
DRAFT = 'D' # the user considers this message a draft; toggled at user discretion.
FLAGGED = 'F' # user-defined flag; toggled at user discretion. 

def inc():
    '''
    1. If the message-id lookup doesn't exist, read everything in "cur" and add to the message-id lookup cache.
    2. Read everything in "new", add it to the message-id cache, and move it to "cur".
    '''
    messageid_path = CSVMap(os.path.expanduser('~/.mhdir-messageid-path'))
    path_messageid = CSVMap(os.path.expanduser('~/.mhdir-path-messageid'))
    for folder in MAILDIR.iterdir():

        # Move stuff from new to cur.
        for mail in (folder / 'new'):
            if ':' in mail.name:
                newname = mail.name
            else:
                newname = mail.name + ':2,'
            mail.rename(folder / 'cur' / newname)

        # Index the stuff in cur.
        for mail in (folder / 'cur').iterdir():
            if str(mail) not in path_messageid:
                with mail.open('rb') as fp:
                    message_id = parse.message_id(fp)
                messageid_path[message_id] = str(mail)
                path_messageid[str(mail)] = message_id

if __name__ == '__main__':
    inc()
