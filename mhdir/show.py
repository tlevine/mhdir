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

from .db import Current

MAILDIR = Path('/Users/t/tom/maildir/hot/_@thomaslevine.com/')

def show(thing,
         showproc = None, showmimeproc = None,
         nocheckmime: bool = False,
         noheader: bool = False,
         draft: bool = False,
         maildir: Path = MAILDIR):

    current = Current(MAILDIR)
    if thing.startswith('+'):
        current.folder = thing[1:]
    else:
        current.message = thing
    if current.message:
        with current.message.open('rb') as fp:
            message_file = message_from_binary_file(fp)
    else:
        print('No messages')

def body():
    def clean_payload(message, payload):
        if 'html' in message.get_content_type().lower():
            payload = clean_html(payload)
        return payload
    def decode_header(header):
        '''
        Decode header with different encodings.
        '''
        def f(content, charset):
            if isinstance(content, str):
                return content
            elif charset == None:
                return content.decode('utf-8')
            else:
                return content.decode(charset)
        return ''.join(f(*args) for args in email.header.decode_header(header))
    def _body(message):
        if message.is_multipart():
            payload = message.get_payload()[0].get_payload(decode = True)
            try:
                body = decode_charset(message, payload)
            except ValueError:
                body = ''
        else:
            body = message.get_payload()
        return clean_payload(message, body)


SHOW_DOC = \
    '''
    :param thing: %s
    :param showproc: Program to display text messages, if you don't want to use the default
    :param showmimeproc: Program to display MIME messages, if you don't want to use the default
    :param nocheckmime: Don't check for MIME messages
    :param noheader: Don't display the header
    :param draft: I don't understand this one.
    '''

from copy import copy
show.__doc__ = SHOW_DOC % 'Folder (+folder) or message (message-id) to display, defaults current message in current folder'
prev = copy(show)
prev.__name__ = 'prev'
prev.__doc__ = SHOW_DOC % 'Folder (+folder) in which to display the previous message, defaults to current folder'
next = copy(show)
next.__name__ = 'next'
next.__doc__ = SHOW_DOC % 'Folder (+folder) in which to display the next message, defaults to current folder'
