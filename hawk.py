# License: This script is public domain.
# Copyright: 2013 Jeena Paradies

import string, random, time, datetime, hmac, hashlib, base64
from urlparse import urlparse


def mkheader(url, http_method, hawk_id, key, app_id=None):

    nonce = mknonce(8)
    parsed_url = urlparse(url)

    n = datetime.datetime.now()
    time_stamp = str(time.mktime(n.timetuple()))

    port = parsed_url.port
    if not port:
        if parsed_url.scheme == "https":
            port = "443"
        else:
            port = "80"

    fragment = ""
    if parsed_url.fragment:
        fragment = "#" + parsed_url.fragment

    app = ""

    if app_id:
        app = ", app=\"" + app_id + "\"" # we need this later in the header

    mac = base64.encodestring(hmac.new(key, normalized_string, hashlib.sha256).digest())

    return 'Hawk id="' + hawk_id + '", mac="' + mac + '", ts="' + time_stamp + '", nonce="' + nonce + '"' + app


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
    normalized_string += "\n" # we don't use ext
    if app_id:
        normalized_string += app_id + "\n"
        normalized_string += "\n" # this is for dlg
    return normalized_string


def mknonce(length=6, chars=(string.ascii_uppercase + string.digits)):
    return ''.join(random.choice(chars) for x in range(length))

if __name__ == "__main__":
    print mkheader("https://example.com/foo/bar?baz=bum#test", "get", "1234", "5678", "abcdef")
