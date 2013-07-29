import requests
import hawk

from registration import RegistrationHelper
from posts import PostUtility


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
