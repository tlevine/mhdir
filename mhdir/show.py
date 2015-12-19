'''
show, prev, next

1. If a folder or message is specified, change the current message.
2. Open the current message with the email module.
3. Display the email in some reasonable way like how nmh does it.
4. Run whatnext

whatnext

'''
from pathlib import Path
from email import message_from_binary_file

from . import parse
from .db import MHDir

MAILDIR = Path('/Users/t/tom/maildir/hot/_@thomaslevine.com/')

def show(increment: ('prev', 'show', 'next'), thing
         showproc = None, showmimeproc = None,
         nocheckmime: bool = False,
         noheader: bool = False,
         draft: bool = False,
         maildir: Path = MAILDIR):

    mhdir = MHDir(maildir)
    if thing.startswith('+'):
        mhdir.folder = thing[1:]
    else:
        mhdir.message = thing

    if mhdir.message:
        if increment in {'prev', 'next'}:
            message.current = prev_cur_next(mhdir.message)[increment]
        with mhdir.message.open('rb') as fp:
            message = message_from_binary_file(fp)
        print(parse.body(message))
    else:
        print('No messages')


SHOW_DOC = \
    '''
    :param thing: %s
    :param showproc: Program to display text messages, if you don't want to use the default
    :param showmimeproc: Program to display MIME messages, if you don't want to use the default
    :param nocheckmime: Don't check for MIME messages
    :param noheader: Don't display the header
    :param draft: I don't understand this one.
    '''
show.__doc__ = SHOW_DOC % 'Folder (+folder) or message (message-id) to display, defaults current message in current folder'
prev.__doc__ = SHOW_DOC % 'Folder (+folder) in which to display the previous message, defaults to current folder'
next.__doc__ = SHOW_DOC % 'Folder (+folder) in which to display the next message, defaults to current folder'
