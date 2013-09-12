import json

import bs4
import requests

from posts import Post


class RegistrationHelper:

    def discover(self, response):
        # Discovery via header field.
        if 'link' in response.headers:
            rel_link = self.get_link_from_header(response.headers)
        # Discovery via HTML doc.
        else:
            soup = bs4.BeautifulSoup(response.text)
            rel_link = soup.head.link.get('href')
        # Return an absolute link.
        if rel_link.startswith("http"):
            link = rel_link
        else:
            link = self.entity_url + rel_link
        return link

    def register(self):
        app_info = {'name': self.name,
                    'scopes': ['permissions'],
                    'url': 'https://app.example.com',
                    'types': {'read': ['https://tent.io/types/app/v0'],
                              'write': ['https://tent.io/types/status/v0',
                                        'https://tent.io/types/photo/v0']},
                    'redirect_uri': 'https://app.example.com/oauth'}
        post = Post('https://tent.io/types/app/v0#', app_info)
        url = self.get_server()['urls']['new_post']
        content_type = 'application/vnd.tent.post.v0+json'
        headers = {'Content-Type': (content_type + '; type="' +
                                    post.post_type + '"')}
        data_dict = {'type': post.post_type, 'content': post.content}
        return requests.post(url, data=json.dumps(data_dict), headers=headers)

    def authorization_request(self):
        oauth_auth = self.get_server()['urls']['oauth_auth']
        temp_app_id = self.reg_json['post']['id']
        payload = {'client_id': temp_app_id}
        return requests.get(oauth_auth, params=payload)

    def access_token_request(self, code):
        oauth_token = self.get_server()['urls']['oauth_token']
        data_dict = {'code': code,
                     'token_type': 'https://tent.io/oauth/hawk-token'}
        data = json.dumps(data_dict)
        content_type = 'application/json'
        headers = {'Accept': content_type, 'Content-Type': content_type}
        return self.make_request(oauth_token, 'POST',
                                 data=data, headers=headers)
