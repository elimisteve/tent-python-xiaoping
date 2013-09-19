import json

import requests

import pyhawk_monkeypatch

from posts import PostUtility
from registration import RegistrationHelper
from utils import GeneralUtility


class TentApp(RegistrationHelper, PostUtility, GeneralUtility):

    def __init__(self, entity_url, app_post):

        # Initial info to set up the app.
        self.entity_url = entity_url
        self.app_post = app_post

        # These will get filled in as we go through registration.
        self.discovery_attachment = None
        self.reg_header = None  # Header of the registration response.
        self.reg_attachment = None  # JSON of the registration response.
        self.credentials_attachment = None
        self.token_header = None
        self.token_attachment = None

        self.id_value = ''
        self.hawk_key = ''
        self.app_id = None

    # Creates an App post on the server and begins filling out this object's
    # attributes.
    #
    # Returns the URL where the user can approve the app.
    def start_setup(self):

        ### Discovery
        response1 = requests.get(self.entity_url)
        response2 = requests.get(self.discover(response1))
        self.discovery_attachment = json.loads(response2.text)

        ### Registration
        response = self.register()
        self.reg_header = dict(response.headers)
        self.reg_attachment = json.loads(response.text)
        self.app_id = self.reg_attachment['post']['id']

        ### Get credentials
        credentials_link = self.get_link_from_header(self.reg_header)
        response = requests.get(credentials_link)
        self.credentials_attachment = json.loads(response.text)

        ### OAuth Authorization Request
        response = self.authorization_request()
        return response.history[0].url

    def finish_setup(self, code):

        self.id_value = self.credentials_attachment['post']['id']
        hawk_key = self.credentials_attachment['post']['content']['hawk_key']
        self.hawk_key = hawk_key.encode('ascii')

        ### Access Token Request
        response = self.access_token_request(code)
        self.token_header = dict(response.headers)
        self.token_attachment = json.loads(response.text)
        self.id_value = self.token_attachment['access_token']
        self.hawk_key = self.token_attachment['hawk_key'].encode('ascii')
