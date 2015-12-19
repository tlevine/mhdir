import os
from pathlib import Path

from . import parse
from .db import MHDir

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
    m = MHDir(MAILDIR)
    for folder in MAILDIR.iterdir():
        if folder.name.startswith('.'):
            continue

        # Move stuff from new to cur.
        for mail in (folder / 'new').iterdir():
            if ':' in mail.name:
                newname = mail.name
            else:
                newname = mail.name + ':2,'
            mail.rename(folder / 'cur' / newname)

        # Index the stuff in cur.
        for mail in (folder / 'cur').iterdir():
            if str(mail) not in m.path_messageid:
                with mail.open('rb') as fp:
                    message_id = parse.message_id(fp)
                m.messageid_path[message_id] = str(mail)
                m.path_messageid[str(mail)] = message_id

if __name__ == '__main__':
    inc()
