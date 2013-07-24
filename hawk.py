# License: This script is public domain.
# Copyright: 2013 Jeena Paradies

import base64
import datetime
import hashlib
import hmac
import random
import string
import time

from urlparse import urlparse


# Nonce and time_stamp are only included as arguments for testing purposes.
def mkheader(url, http_method, hawk_id, key, attachment_hash=None, app_id=None,
             nonce=None, time_stamp=None):

    if not nonce:
        nonce = mknonce(8)
    parsed_url = urlparse(url)

    if not time_stamp:
        n = datetime.datetime.now()
        time_stamp = str(time.mktime(n.timetuple()))

    port = parsed_url.port
    if not port:
        if parsed_url.scheme == 'https':
            port = '443'
        else:
            port = '80'

    fragment = ''
    if parsed_url.fragment:
        fragment = '#' + parsed_url.fragment

    hash_str = ''
    if attachment_hash:
        hash_str = ", hash=\"" + attachment_hash + "\""

    app = ''
    if app_id:
        app = ", app=\"" + app_id + "\""

    normalized_string = mk_normalized_string(time_stamp, nonce, http_method,
                                             parsed_url, fragment, port,
                                             attachment_hash=attachment_hash,
                                             app_id=app_id)
    mac = mk_mac(key, normalized_string)

    return ('Hawk id="' + hawk_id + '", mac="' + mac + '", ts="'
            + time_stamp + '", nonce="' + nonce + '"' + hash_str + app)


def mk_normalized_string(time_stamp, nonce, http_method, parsed_url, fragment,
                         port, attachment_hash=None, app_id=None):
    normalized_string = ("hawk.1.header\n"
                         + time_stamp + "\n"
                         + nonce + "\n"
                         + http_method.upper() + "\n"
                         + parsed_url.path + parsed_url.query + fragment + "\n"
                         + parsed_url.hostname.lower() + "\n"
                         + str(port) + "\n")
    if attachment_hash:
        normalized_string += attachment_hash + "\n"
    normalized_string += "\n"  # We don't use ext.
    if app_id:
        normalized_string += app_id + "\n"
        normalized_string += "\n"  # This is for dlg.
    return normalized_string


def mk_mac(key, normalized_string):
    new_hmac = hmac.new(key, normalized_string, hashlib.sha256).digest()
    return base64.b64encode(new_hmac)


def mknonce(length=6, chars=(string.ascii_uppercase + string.digits)):
    return ''.join(random.choice(chars) for x in range(length))
