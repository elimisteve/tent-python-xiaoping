import json
import os
import sys
import unittest

from hawk.client import header
from hawk.hcrypto import calculate_payload_hash

file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(file_path))
sys.path.append(os.path.join(project_dir, 'xiaoping'))
import pyhawk_monkeypatch


# Note that this doesn't test time stamp, nonce, or hash creation.
class TestHeaderCreation(unittest.TestCase):

    def test_app_request_with_hash(self):
        # Test data
        self.url = 'https://example.com/posts'
        self.hawk_id = 'exqbZWtykFZIh2D7cXi9dA'
        self.key = 'HX9QcbD-r3ItFEnRcAuOSg'
        self.time_stamp = 1368996800
        self.nonce = '3yuYCD4Z'
        self.http_method = 'post'
        self.fragment = ''
        self.attachment_hash = 'neQFHgYKl/jFqDINrC21uLS0gkFglTz789rzcSr7HYU='
        self.app_id = 'wn6yzHGe5TLaT-fvOPbAyQ'

        # Answers
        self.correct_header = ('Hawk id="exqbZWtykFZIh2D7cXi9dA", mac="2sttHC'
                               'QJG9ejj1x7eCi35FP23Miu9VtlaUgwk68DTpM=", ts="'
                               '1368996800", nonce="3yuYCD4Z", hash="neQFHgYK'
                               'l/jFqDINrC21uLS0gkFglTz789rzcSr7HYU=", app="w'
                               'n6yzHGe5TLaT-fvOPbAyQ"')
        self.other_order = ('Hawk id="exqbZWtykFZIh2D7cXi9dA", ts="1368996800'
                            '", nonce="3yuYCD4Z", hash="neQFHgYKl/jFqDINrC21u'
                            'LS0gkFglTz789rzcSr7HYU=", mac="2sttHCQJG9ejj1x7e'
                            'Ci35FP23Miu9VtlaUgwk68DTpM=", app="wn6yzHGe5TLaT'
                            '-fvOPbAyQ"')
        self.various_orders = [self.correct_header, self.other_order]

        # Run code
        created_header = self.get_header()
        self.assertIn(created_header, self.various_orders)

    def get_header(self):
        url = self.url
        method = self.http_method
        credentials = {'id': self.hawk_id,
                       'key': self.key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'timestamp': self.time_stamp,
                   'nonce': self.nonce,
                   'app': self.app_id,
                   'ext': ''}
        if hasattr(self, 'attachment_hash'):
            options['hash'] = self.attachment_hash
        elif hasattr(self, 'data'):
            options['payload'] = self.data
            options['contentType'] = self.content_type
        return header(url, method, options=options)['field']

if __name__ == '__main__':
    unittest.main()
