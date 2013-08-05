import json
import os
import sys
import unittest

from hawk.client import header
from hawk.hcrypto import calculate_payload_hash

import pyhawk_monkeypatch


# Test against examples of header creation from here:
# https://tent.io/docs/authentication
#
# Note that this doesn't test time stamp, nonce, or hash creation.
class TestTentDocExamples(unittest.TestCase):

    def setUp(self):
        # Shared test data
        self.key = 'HX9QcbD-r3ItFEnRcAuOSg'
        self.url = 'https://example.com/posts'
        self.http_method = 'POST'

    def test_app_request_with_hash(self):
        # More test data
        self.hawk_id = 'exqbZWtykFZIh2D7cXi9dA'
        self.time_stamp = 1368996800
        self.nonce = '3yuYCD4Z'
        self.attachment_hash = 'neQFHgYKl/jFqDINrC21uLS0gkFglTz789rzcSr7HYU='
        self.app_id = 'wn6yzHGe5TLaT-fvOPbAyQ'
        # Answers
        self.correct = ['id="exqbZWtykFZIh2D7cXi9dA"',
                        'mac="2sttHCQJG9ejj1x7eCi35FP23Miu9VtlaUgwk68DTpM="',
                        'ts="1368996800"',
                        'nonce="3yuYCD4Z"',
                        'hash="neQFHgYKl/jFqDINrC21uLS0gkFglTz789rzcSr7HYU="',
                        'app="wn6yzHGe5TLaT-fvOPbAyQ"']
        # Run code
        self.assertTrue(self.check_header(self.get_header(), self.correct))

    def test_relationship_request(self):
        # More test data
        self.hawk_id = 'exqbZWtykFZIh2D7cXi9dA'
        self.time_stamp = 1368996800
        self.nonce = '3yuYCD4Z'
        # Answers
        self.correct = ['id="exqbZWtykFZIh2D7cXi9dA"',
                        'mac="OO2ldBDSw8KmNHlEdTC4BciIl8+uiuCRvCnJ9KkcR3Y="',
                        'ts="1368996800"',
                        'nonce="3yuYCD4Z"']
        # Run code
        self.assertTrue(self.check_header(self.get_header(), self.correct))

    def get_header(self):
        url = self.url
        method = self.http_method
        credentials = {'id': self.hawk_id,
                       'key': self.key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'timestamp': self.time_stamp,
                   'nonce': self.nonce,
                   'ext': ''}
        if hasattr(self, 'attachment_hash'):
            options['hash'] = self.attachment_hash
        if hasattr(self, 'app_id'):
            options['app'] = self.app_id
        return header(url, method, options=options)['field']

    # Takes a header string and a list of the contents that should make it up.
    #
    # Parses the header by removing each item in the contents list one at a
    # time. If the header doesn't include one of the items or if it has
    # leftover content remaining at the end besides spaces and commas,
    # the header and correct_contents don't match.
    def check_header(self, header, correct_contents):
        if header.startswith('Hawk '):
            header = header[len('Hawk '):]
        else:
            return False
        for i in correct_contents:
            if i in header:
                header = header.replace(i, '', 1)
            else:
                return False
        header = header.replace(' ', '')
        header = header.replace(',', '')
        if header != '':
            return False
        else:
            return True

if __name__ == '__main__':
    unittest.main()
