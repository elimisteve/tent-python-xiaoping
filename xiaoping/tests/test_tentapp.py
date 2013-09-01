import os
import sys
import unittest

import registration
from tentapp import TentApp


file_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))

entity_path = os.path.join(project_path, 'data_for_testing', 'entity_url')
entity_url = open(entity_path).read().rstrip()

info_path = os.path.join(project_path, 'data_for_testing', 'registration.json')
registration_json = open(info_path).read()


class FunctionalTentAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global app
        app = TentApp(entity_url, registration_json)
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
