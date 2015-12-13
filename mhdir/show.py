def show(thing,
         showproc = None, showmimeproc = None,
         nocheckmime: bool = False,
         noheader: bool = False,
         draft: bool = False):

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
show.__doc__ = SHOW_DOC % 'Folder (+folder) or message to display, defaults current message in current folder'
prev = copy(show)
prev.__name__ = 'prev'
prev.__doc__ = SHOW_DOC % 'Folder (+folder) in which to display the previous message, defaults to current folder'
next = copy(show)
next.__name__ = 'next'
next.__doc__ = SHOW_DOC % 'Folder (+folder) in which to display the next message, defaults to current folder'

def repl(
