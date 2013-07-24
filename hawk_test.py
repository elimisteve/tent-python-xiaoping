import unittest
import urlparse

from hawk import mk_normalized_string, mk_mac


class TestHawk(unittest.TestCase):

    def test_mk_normalized_string(self):
        time_stamp = '1368996800'
        nonce = '3yuYCD4Z'
        http_method = 'post'
        parsed_url = urlparse.urlparse('http://example.com/posts')
        fragment = ''
        port = '443'
        attachment_hash = 'neQFHgYKl/jFqDINrC21uLS0gkFglTz789rzcSr7HYU='
        app_id = 'wn6yzHGe5TLaT-fvOPbAyQ'
        normalized = mk_normalized_string(time_stamp, nonce, http_method,
                                          parsed_url, fragment, port,
                                          attachment_hash, app_id)
        self.assertEquals(normalized,
                          'hawk.1.header\n1368996800\n3yuYCD4Z\nPOST\n/posts'
                          '\nexample.com\n443\nneQFHgYKl/jFqDINrC21uLS0gkFgl'
                          'Tz789rzcSr7HYU=\n\nwn6yzHGe5TLaT-fvOPbAyQ\n\n')

    def test_mk_mac(self):
        key = 'HX9QcbD-r3ItFEnRcAuOSg'
        mac = mk_mac(key,
                     'hawk.1.header\n1368996800\n3yuYCD4Z\nPOST\n/posts'
                     '\nexample.com\n443\nneQFHgYKl/jFqDINrC21uLS0gkFgl'
                     'Tz789rzcSr7HYU=\n\nwn6yzHGe5TLaT-fvOPbAyQ\n\n')
        self.assertEquals(mac, '2sttHCQJG9ejj1x7eCi35FP23Miu9VtlaUgwk68DTpM=')

if __name__ == '__main__':
    unittest.main()
