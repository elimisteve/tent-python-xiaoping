import os
import sys
import unittest

file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(file_path))
sys.path.append(os.path.join(project_dir, 'xiaoping'))
from tentapp import TentApp


entity_url = open('test_info/entity_url').read().rstrip()
registration_json = open('test_info/registration.json').read()
app = TentApp(entity_url, registration_json)


class TestTentApp(unittest.TestCase):

    def test_setup(self):
        app.setup()
        self.assertTrue(app.token_attachment)

if __name__ == '__main__':
    unittest.main()
