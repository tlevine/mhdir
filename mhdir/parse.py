import logging
import re

from lxml.html.clean import clean_html

logger = logging.getLogger(__name__)

MESSAGE_ID = re.compile(br'^message-id: <([^>]*)> *$', flags = re.IGNORECASE)

def message_id(fp):
    for line in fp:
        m = re.match(MESSAGE_ID, line)
        if m:
            return m.group(1).decode('ascii')
    else:
        logger.warning('No message-id in %s' % fp.name)

def body(message):
    if message.is_multipart():
        payload = message.get_payload()[0].get_payload(decode = True)
        try:
            body = decode_charset(message, payload)
        except ValueError:
            body = ''
    else:
        body = message.get_payload()

    if 'html' in message.get_content_type().lower():
        body = clean_html(body)
    return body
