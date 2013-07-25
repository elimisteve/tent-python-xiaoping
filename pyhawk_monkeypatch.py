import hawk


HAWK_VER = 1


# Code modified from commit 60eb3f2c299975d61d732a4fc9477ee6e601644b of
# https://github.com/mozilla/PyHawk
def modified_normalize_string(mac_type, options):
    """Serializes mac_type and options into a HAWK string."""

    if 'hash' not in options or options['hash'] is None:
        options['hash'] = ''

    normalized = '\n'.join(
        ['hawk.' + str(HAWK_VER) + '.' + mac_type,
         str(options['ts']),
         options['nonce'],
         options['method'].upper(),
         options['resource'],
         options['host'].lower(),
         str(options['port']),
         options['hash']])

    normalized += '\n'

    if 'ext' in options and len(options['ext']) > 0:
        n_ext = options['ext'].replace('\\', '\\\\').replace('\n', '\\n')
        normalized += n_ext

    normalized += '\n'

    if 'app' in options and options['app'] is not None and \
       len(options['app']) > 0:
        normalized += options['app'] + '\n'
        if 'dlg' in options and options['dlg'] is not None:  # monkeypatch
            if 'dlg' in options and len(options['dlg']) > 0:
                normalized += options['dlg'] + '\n'

    normalized += '\n'  # more monkeypatching

    return normalized

hawk.hcrypto.normalize_string = modified_normalize_string
