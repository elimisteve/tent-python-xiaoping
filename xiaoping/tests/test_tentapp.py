import os
import sys
import unittest

from tentapp import TentApp


file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
entity_path = os.path.join(project_dir, 'data_for_testing', 'entity_url')
info_path = os.path.join(project_dir, 'data_for_testing', 'registration.json')


class TestTentApp(unittest.TestCase):

    def setUp(self):
        entity_url = open(entity_path).read().rstrip()
        registration_json = open(info_path).read()
        self.app = TentApp(entity_url, registration_json)
        self.app.setup()

    def test_setup(self):
        self.assertTrue(self.app.token_attachment)

    def test_post_status(self):
        response = self.app.post_status('test status')
        self.assertTrue(response)

if __name__ == '__main__':
    unittest.main()
