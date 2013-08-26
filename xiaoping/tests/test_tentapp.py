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


class UnitTests(unittest.TestCase):

    def setUp(self):
        global app
        app = TentApp(entity_url, registration_json)

    def test_discover(self):
        correct = ('http://localhost:8080/tent/posts/http%3A%2F%2Flocalhost%3A'
                   '8080%2Ftent/Omrxar1tLKvqQE5hKgl9lQ')
        class Response:
            pass
        response = Response()
        response.headers = {'link': ('<http://localhost:8080/tent/posts/http%3'
                                     'A%2F%2Flocalhost%3A8080%2Ftent/Omrxar1tL'
                                     'KvqQE5hKgl9lQ>; rel="https://tent.io/rel'
                                     's/meta-post"')}
        link = app.discover(response)
        self.assertEqual(correct, link)

    def test_register(self):
        correct_url = u'http://localhost:8080/tent/posts'
        correct_headers = {'Content-Type': ('application/vnd.tent.post.v0+json'
                                            '; type="https://tent.io/types/app'
                                            '/v0#"')}
        app.discovery_attachment = (
            {'post': {'content': {'servers': [{'urls': {'new_post':
            u'http://localhost:8080/tent/posts'}}]}}}
        )
        url, kwargs = app.register()
        headers = kwargs['headers']
        self.assertEqual(correct_url, url)
        self.assertEqual(correct_headers, headers)

    def test_authorization_request(self):
        correct_url = u'http://localhost:8080/tent/oauth/authorize'
        correct_payload = {'client_id': u'pwS5ZWmOnURk_SteaFzCVA'}
        app.discovery_attachment = (
            {'post': {'content': {'servers': [{'urls': {'oauth_auth':
            u'http://localhost:8080/tent/oauth/''authorize'}}]}}}
        )
        app.reg_json = {'post': {'id': u'pwS5ZWmOnURk_SteaFzCVA'}}
        url, kwargs = app.authorization_request()
        payload = kwargs['params']
        self.assertEqual(correct_url, url)
        self.assertEqual(correct_payload, payload)

    def test_access_token_request(self):
        correct_args = (u'http://localhost:8080/tent/oauth/token', 'POST')
        correct_data = ('{"token_type": "https://tent.io/oauth/hawk-token", "c'
                        'ode": "e3b940d1875c6069bc3c681669c1bee444d94cd422b5aa'
                        '431c03327ac21dd417"}')
        correct_headers = {'Content-Type': 'application/json',
                           'Accept': 'application/json'}
        code = ('e3b940d1875c6069bc3c681669c1bee4'
                '44d94cd422b5aa431c03327ac21dd417')
        app.discovery_attachment = (
            {'post': {'content': {'servers': [{'urls': {'oauth_token':
            u'http://localhost:8080/tent/oauth/token'}}]}}}
        )
        args, kwargs = app.access_token_request(code)
        self.assertEqual(correct_args, args)
        self.assertEqual(correct_data, kwargs['data'])
        self.assertEqual(correct_headers, kwargs['headers'])

if __name__ == '__main__':
    unittest.main()
