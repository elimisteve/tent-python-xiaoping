import unittest
import urlparse

from hawk import mkheader, mk_normalized_string, mk_mac, mk_payload_digest


# Note that this currently doesn't test either time stamp or nonce creation.
class TestAppRequestWithHash(unittest.TestCase):

    def setUp(self):
        # Test data
        self.url = 'https://example.com/posts'
        self.hawk_id = 'exqbZWtykFZIh2D7cXi9dA'
        self.key = 'HX9QcbD-r3ItFEnRcAuOSg'
        self.time_stamp = '1368996800'
        self.nonce = '3yuYCD4Z'
        self.http_method = 'post'
        self.fragment = ''
        self.port = '443'
        self.attachment_hash = 'neQFHgYKl/jFqDINrC21uLS0gkFglTz789rzcSr7HYU='
        self.app_id = 'wn6yzHGe5TLaT-fvOPbAyQ'

        # Answers
        self.correct_normalized = ('hawk.1.header\n1368996800\n3yuYCD4Z\nPOST'
                                   '\n/posts\nexample.com\n443\nneQFHgYKl/jFq'
                                   'DINrC21uLS0gkFglTz789rzcSr7HYU=\n\nwn6yzH'
                                   'Ge5TLaT-fvOPbAyQ\n\n')
        self.correct_mac = '2sttHCQJG9ejj1x7eCi35FP23Miu9VtlaUgwk68DTpM='
        self.correct_header = ('Hawk id="exqbZWtykFZIh2D7cXi9dA", mac="2sttHC'
                               'QJG9ejj1x7eCi35FP23Miu9VtlaUgwk68DTpM=", ts="'
                               '1368996800", nonce="3yuYCD4Z", hash="neQFHgYK'
                               'l/jFqDINrC21uLS0gkFglTz789rzcSr7HYU=", app="w'
                               'n6yzHGe5TLaT-fvOPbAyQ"')

    def test_mk_normalized_string(self):
        parsed_url = urlparse.urlparse(self.url)
        normalized = mk_normalized_string(self.time_stamp, self.nonce,
                                          self.http_method, parsed_url,
                                          self.fragment, self.port,
                                          self.attachment_hash, self.app_id)
        self.assertEquals(normalized, self.correct_normalized)

    def test_mk_mac(self):
        mac = mk_mac(self.key, self.correct_normalized)
        self.assertEquals(mac, self.correct_mac)

    def test_mkheader(self):
        header = mkheader(self.url, self.http_method, self.hawk_id, self.key,
                          nonce=self.nonce, time_stamp=self.time_stamp,
                          attachment_hash=self.attachment_hash,
                          app_id=self.app_id)
        self.assertEquals(header, self.correct_header)


class TestStandaloneFunctions(unittest.TestCase):

    def test_mk_payload_digest(self):
        content_type = 'text/plain'
        data = 'Thank you for flying Hawk'
        payload_digest = mk_payload_digest(content_type, data)
        correct_payload_digest = ('hawk.1.payload\ntext/plain\n'
                                  'Thank you for flying Hawk\n')
        self.assertEquals(payload_digest, correct_payload_digest)

if __name__ == '__main__':
    unittest.main()
