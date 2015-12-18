import re

MESSAGE_ID = re.compile(r'^message-id: *(.*)$')

def message_id(fp):
    for line in fp:
        m = re.match(MESSAGE_ID, line)
        if m:
            return m.group(1)
