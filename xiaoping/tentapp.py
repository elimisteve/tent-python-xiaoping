import json
import urlparse

import hawk
import requests

from registration import RegistrationHelper
from posts import PostUtility
import pyhawk_monkeypatch


class TentApp(RegistrationHelper, PostUtility):

    def __init__(self, entity_url, registration_json):

        # Initial info to set up the app.
        self.entity_url = entity_url
        self.app_info = registration_json

        # These will get filled in as we go through registration.
        self.discovery_attachment = None
        self.reg_header = None  # Header of the registration response.
        self.reg_attachment = None  # JSON of the registration response.
        self.credentials = None
        self.token_header = None
        self.token_attachment = None

        self.id_value = None
        self.hawk_key = None
        self.app_id = None

    # Creates an app post on the server and fills out
    # the instance's attributes.
    def setup(self):

        ### Discovery
        response1 = requests.get(self.entity_url)
        response2 = requests.get(self.discover(response1))
        self.discovery_attachment = json.loads(response2.text)

        ### Registration
        url, kwargs = self.register()
        response = requests.post(url, **kwargs)
        self.reg_header = dict(response.headers)
        self.reg_json = json.loads(response.text)
        self.app_id = self.reg_json['post']['id']

        ### Get credentials
        credentials_link = self.get_link_from_header(self.reg_header)
        response = requests.get(credentials_link)
        self.credentials_attachment = json.loads(response.text)

        ### OAuth Authorization Request
        url, kwargs = self.authorization_request()
        response = requests.get(url, **kwargs)
        location = response.history[0].headers.get('location')
        parsed_location = urlparse.urlparse(location)
        code = urlparse.parse_qs(parsed_location.query)['code'][0]

        ### Access Token Request
        self.id_value = self.reg_json['post']['mentions'][0]['post']
        hawk_key = self.credentials_attachment['post']['content']['hawk_key']
        self.hawk_key = hawk_key.encode('ascii')
        args, kwargs = self.access_token_request(code)
        response = self.make_request(*args, **kwargs)
        self.token_header = dict(response.headers)
        self.token_attachment = json.loads(response.text)
        self.id_value = self.token_attachment['access_token']
        self.hawk_key = self.token_attachment['hawk_key'].encode('ascii')

    # A wrapper around PyHawk's header creator and requests.get/requests.post
    # to make them easy to use within Xiaoping.
    def make_request(self, url, method, headers=[], data=None):
        credentials = {'id': self.id_value,
                       'key': self.hawk_key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'app': self.app_id,
                   'ext': ''}
        if 'payload' in options:
            options['payload'] = data
            options['contentType'] = content_type
            options['dlg'] = ''
        header = hawk.client.header(url, method, options=options)['field']
        headers['Authorization'] = header
        if method.upper() == 'GET':
            return requests.get(url, headers=headers)
        if method.upper() == 'POST':
            return requests.post(url, data=data, headers=headers)
