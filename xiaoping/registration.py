import json

import bs4
import hawk
import requests


class RegistrationHelper:

    # TODO There should be a library that can handle this.
    def get_link_from_header(self, header):
        link_header = header['link']
        left, right = link_header.find('<') + 1, link_header.find('>')
        return link_header[left:right]

    def get_server(self):
        # TODO Should iterate through servers_list
        # in case there's more than one.
        return self.discovery_attachment['post']['content']['servers'][0]

    def discover(self, response):
        # Discovery via header field.
        if response.headers['link']:
            rel_link = self.get_link_from_header(response.headers)
            if rel_link.startswith("http"):
                link = rel_link
            else:
                link = self.entity_url + rel_link
        # Discovery via HTML doc.
        else:
            soup = bs4.BeautifulSoup(response.text)
            link = soup.head.link.get('href')
        return link

    def register(self):
        new_post = self.get_server()['urls']['new_post']
        headers = {'Content-Type': ('application/vnd.tent.post.v0+json;'
                                    ' type="https://tent.io/types/app/v0#"')}
        return (new_post, {'data': self.app_info, 'headers': headers})

    def authorization_request(self):
        oauth_auth = self.get_server()['urls']['oauth_auth']
        temp_app_id = self.reg_json['post']['id']
        payload = {'client_id': temp_app_id}
        return (oauth_auth, {'params': payload})

    def make_request(self, url, method, headers=[], data=None):
        options = {'credentials': credentials,
                   'app': self.app_id,
                   'ext': ''}
        if 'payload' in options:
            options['payload'] = data
            options['contentType'] = content_type
            options['dlg'] = ''
        header = hawk.client.header(url, method, options=options)['field']

    def access_token_request(self, code):
        oauth_token = self.get_server()['urls']['oauth_token']
        data_dict = {'code': code,
                     'token_type': 'https://tent.io/oauth/hawk-token'}
        data = json.dumps(data_dict)
        content_type = 'application/json'
        headers = {'Accept': content_type, 'Content-Type': content_type}
        return ((oauth_token, 'POST'), {'data': data, 'headers': headers})
