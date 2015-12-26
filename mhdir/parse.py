import logging
import re

try:
    from lxml.html.clean import clean_html
except ImportError:
    def clean_html(x):
        logger.warning('Install lxml if you want to fix this email message.')
        return x
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
        if payload:
            try:
                body = decode_charset(message, payload)
            except ValueError:
                body = ''
        else:
            body = message.get_payload()[0]
    else:
        body = message.get_payload()

    if 'html' in message.get_content_type().lower():
        body = clean_html(body)
    return body

def decode_charset(message, payload):
    '''
    Decode a payload and clean the HTML if appropriate.
    '''
    base_charsets = []
    charsets = list(filter(None, message.get_charsets()))
    for charset in charsets + base_charsets:
        try:
            return payload.decode(charset)
        except UnicodeDecodeError:
            pass
    raise ValueError('Could not determine charset')
