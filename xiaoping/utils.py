import hawk
import requests


class GeneralUtility:

    # A wrapper around PyHawk's header creator and requests.get/requests.post
    # to make them easy to use within Xiaoping.
    def make_request(self, url, method, headers=None, data=None):
        if headers is None:
            headers = []
        headers['Authorization'] = self.make_auth_header(url, method)
        if method.upper() == 'GET':
            return requests.get(url, headers=headers)
        if method.upper() == 'POST':
            return requests.post(url, data=data, headers=headers)

    # The kwargs are for testing purposes only.
    def make_auth_header(self, url, method, timestamp=None, nonce=None,
                         attachment_hash=None):
        credentials = {'id': self.id_value,
                       'key': self.hawk_key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'ext': ''}
        if hasattr(self, 'app_id'):
            options['app'] = self.app_id
        # Begin testing use only.
        if timestamp:
            options['timestamp'] = timestamp
        if nonce:
            options['nonce'] = nonce
        if attachment_hash:
            options['hash'] = attachment_hash
        # End testing use only.
        return hawk.client.header(url, method, options=options)['field']

    # TODO There should be a library that can handle this.
    def get_link_from_header(self, header):
        link_header = header['link']
        left, right = link_header.find('<') + 1, link_header.find('>')
        return link_header[left:right]

    def get_server(self):
        # TODO Should iterate through servers_list
        # in case there's more than one.
        return self.discovery_attachment['post']['content']['servers'][0]
