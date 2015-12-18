import logging
import re

logger = logging.getLogger(__name__)

MESSAGE_ID = re.compile(br'^message-id: <([^>]*)> *$', flags = re.IGNORECASE)

def message_id(fp):
    for line in fp:
        m = re.match(MESSAGE_ID, line)
        if m:
            return m.group(1).decode('ascii')
    else:
        logger.warning('No message-id in fp.name')
