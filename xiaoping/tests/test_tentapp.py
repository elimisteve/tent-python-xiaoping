import unittest

import config
import registration
from tentapp import TentApp


class FunctionalTentAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global app
        app = TentApp(config.test_entity, 'Xiaoping Tester')
        link = app.start_setup()
        print 'Go to the link, click accept, and enter the "code" part'
        print 'of the url argument here.'
        print link
        code = raw_input('> ')
        app.finish_setup(code)

    def test_setup(self):
        self.assertTrue(app.token_attachment)

    def test_post_status(self):
        response = app.post_status('Test post.')
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
