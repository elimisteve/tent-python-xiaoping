import sys
import unittest

from tentapp import TentApp


entity_url = sys.argv[1]
app = TentApp(entity_url)


class TestTentApp(unittest.TestCase):

    def test_discovery(self):
        app.discover()
        self.assertTrue(app.new_post)

    def test_registration(self):
        app.register(app.new_post)
        self.assertTrue(app.registration_response_header)
        self.assertTrue(app.registration_response_text)

if __name__ == '__main__':
    sys.argv = sys.argv[:1]
    unittest.main()
