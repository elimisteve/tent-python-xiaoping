import os
import sys
import unittest

file_path = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(file_path))
sys.path.append(os.path.join(project_dir, 'xiaoping'))
from tentapp import TentApp


entity_url = sys.argv[1]
app = TentApp(entity_url)


class TestTentApp(unittest.TestCase):

    def test_setup(self):
        app.setup()
        self.assertTrue(app.token_response)

if __name__ == '__main__':
    sys.argv = sys.argv[:1]
    unittest.main()
