from . import parse

MAILDIR = Path('/Users/t/tom/maildir/hot/_@thomaslevine.com/')

def inc():
    '''
    1. If the message-id lookup doesn't exist, read everything in "cur" and add to the message-id lookup cache.
    2. Read everything in "new", add it to the message-id cache, and move it to "cur".
    '''
    for folder in p.iterdir():
        for mail in (folder / 'cur').iterdir():
            with mail.open() as fp:
                message_id = parse.message_id(fp)
            
