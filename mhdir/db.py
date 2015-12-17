import os

from persistent import Persistent
import ZODB, ZODB.FileStorage

DIR = os.path.expanduser('~/.mhdir')
os.makedirs(DIR, exist_ok = True)
DB = os.path.join(DIR, 'db')
MAILDIR = os.path.join(os.path.expanduser('~'), 'safe', 'maildir', 'hot', '_@thomaslevine.com')

class Folder(Persistent):
    def __init__(self, path, current = None):
        self.current = current
        self.path = path
    def __repr__(self):
        return 'Folder(%s, current = %s)' % (repr(self.path), repr(self.current))

storage = ZODB.FileStorage.FileStorage(DB)
db = ZODB.DB(storage)
connection = db.open()
dbroot = connection.root()

from BTrees.OOBTree import OOBTree
if 'folders' not in dbroot:
    dbroot['folders'] = OOBTree()

for folder in ['INBOX', 'Sent']:
    if folder not in dbroot['folders']:
        dbroot['folders'][folder] = Folder(os.path.join(MAILDIR, folder))

print(dbroot['folders']['INBOX'])
dbroot['folders']['INBOX'].current = 'aoeu'

#import transaction
#transaction.commit()
#storage.close()
