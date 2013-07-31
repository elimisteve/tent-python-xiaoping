import hawk
import requests


class GeneralUtility:

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

    # TODO There should be a library that can handle this.
    def get_link_from_header(self, header):
        link_header = header['link']
        left, right = link_header.find('<') + 1, link_header.find('>')
        return link_header[left:right]

    def get_server(self):
        # TODO Should iterate through servers_list
        # in case there's more than one.
        return self.discovery_attachment['post']['content']['servers'][0]
