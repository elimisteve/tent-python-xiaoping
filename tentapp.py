import json
import sys
import urlparse

import bs4
import requests


class TentApp:

    def __init__(self, entity_url):
        self.entity_url = entity_url
        self.discovery_response = None
        self.registration_header = None
        self.registration_attachment = None

    def setup(self):
        self.discovery_response = self.discover(self.entity_url)
        app_info = open('registration.json').read()
        servers_list = self.discovery_response['post']['content']['servers']
        # TODO Should iterate through servers_list
        # in case there's more than one.
        new_post = servers_list[0]['urls']['new_post']
        (self.registration_header,
         self.registration_attachment) = self.register(app_info, new_post)
        id_value = self.registration_attachment['post']['id']
        oauth_auth = servers_list[0]['urls']['oauth_auth']
        code = self.authorization_request(oauth_auth, id_value)

    # Returns the discovery response attachment as a dictionary.
    def discover(self, entity_url):
        response = requests.get(entity_url)
        # Discovery via header field.
        if response.headers['link']:
            link_header = response.headers['link']
            # TODO This should use an actual HTML parsing library.
            left, right = link_header.find('<') + 1, link_header.find('>')
            rel_link = link_header[left:right]
            link = entity_url + rel_link
        # Discovery via HTML doc.
        else:
            soup = bs4.BeautifulSoup(response.text)
            link = soup.head.link.get('href')
        discovery_string = requests.get(link)
        return json.loads(discovery_string.text)

    # Returns the registration response header as a string
    # and the response attachment as a dictionary.
    def register(self, app_info, new_post):
        headers = {'Content-Type': ('application/vnd.tent.post.v0+json;'
                                    ' type="https://tent.io/types/app/v0#"')}
        post_creation_response = requests.post(new_post, data=app_info,
                                               headers=headers)
        registration_header = str(post_creation_response.headers)
        registration_attachment = json.loads(post_creation_response.text)
        return registration_header, registration_attachment

    # Returns the code parameter in the form of a string.
    def authorization_request(self, oauth_auth, id_value):
        payload = {'client_id': id_value}
        response = requests.get(oauth_auth, params=payload)
        location = response.history[0].headers.get('location')
        parsed_location = urlparse.urlparse(location)
        return urlparse.parse_qs(parsed_location.query)['code']
