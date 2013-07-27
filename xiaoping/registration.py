import json
import urlparse

import bs4
import hawk
import requests

import pyhawk_monkeypatch


class PreRegistration:

    # TODO There should be a library that can handle this.
    def get_link_from_header(self, header):
        link_header = header['link']
        left, right = link_header.find('<') + 1, link_header.find('>')
        return link_header[left:right]

    # Returns the discovery response attachment as a dictionary.
    def discover(self, entity_url):
        response = requests.get(entity_url)
        # Discovery via header field.
        if response.headers['link']:
            rel_link = self.get_link_from_header(response.headers)
            if rel_link.startswith("http"):
                link = rel_link
            else:
                link = entity_url + rel_link
        # Discovery via HTML doc.
        else:
            soup = bs4.BeautifulSoup(response.text)
            link = soup.head.link.get('href')
        discovery_string = requests.get(link)
        return json.loads(discovery_string.text)

    # Creates an app post on the server.
    #
    # Returns the registration response header and the response attachment
    # as dictionaries.
    def register(self, app_info, new_post):
        headers = {'Content-Type': ('application/vnd.tent.post.v0+json;'
                                    ' type="https://tent.io/types/app/v0#"')}
        post_creation_response = requests.post(new_post, data=app_info,
                                               headers=headers)
        registration_header = dict(post_creation_response.headers)
        registration_attachment = json.loads(post_creation_response.text)
        return registration_header, registration_attachment

    # Returns the app's credentials as a dictionary.
    def get_credentials(self, credentials_link):
        response = requests.get(credentials_link)
        return json.loads(response.text)

    # Returns the code parameter in the form of a string.
    def authorization_request(self, oauth_auth, app_id):
        payload = {'client_id': app_id}
        response = requests.get(oauth_auth, params=payload)
        location = response.history[0].headers.get('location')
        parsed_location = urlparse.urlparse(location)
        return urlparse.parse_qs(parsed_location.query)['code'][0]

    def access_token_request(self, url, code, id_value, hawk_key, app_id):
        content_type = 'application/json'
        data_dict = {'code': code,
                     'token_type': 'https://tent.io/oauth/hawk-token'}
        data = json.dumps(data_dict)
        credentials = {'id': id_value,
                       'key': hawk_key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'payload': data,
                   'contentType': 'application/json',
                   'app': app_id,
                   'ext': '',
                   'dlg': ''}
        header = hawk.client.header(url, 'POST', options=options)['field']
        headers = {'Accept': 'application/json',
                   'Authorization': header,
                   'Content-Type': content_type}
        response = requests.post(url, data=data, headers=headers)
        return dict(response.headers), json.loads(response.text)
