def comp():
    raise NotImplementedError('Interactivity is annoying.')

def inc():
    print('Just run offlineimap.')

def show(folder = None, msg = None,
         showproc = None, showmimeproc = None,
         nocheckmime: bool = False,
         noheader: bool = False,
         draft: bool = False):
    '''
    :param folder: Folder to display, defaults to current folder
    :param msg: Message to display, defaults to cur
    :param showproc: Program to display text messages, if you don't want to use the default
    :param showmimeproc: Program to display MIME messages, if you don't want to use the default
    :param nocheckmime: Don't check for MIME messages
    :param noheader: Don't display the header
    :param draft: I don't understand this one.
    '''

DEFAULT_FROM = 'Thomas Levine <_@thomaslevine.com>'

def mhmail(to: list = None, cc: list = None, FROM = DEFAULT_FROM,
           headerfield: list = None,
           subject = None, body = None, attach: list = None,
           nosend: bool = False):
    '''

    '''
