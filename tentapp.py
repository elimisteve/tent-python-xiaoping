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
        self.credentials = None

    def setup(self):

        # Discovery
        self.discovery_response = self.discover(self.entity_url)

        # Registration
        app_info = open('registration.json').read()
        servers_list = self.discovery_response['post']['content']['servers']
        # TODO Should iterate through servers_list
        # in case there's more than one.
        new_post = servers_list[0]['urls']['new_post']
        (self.registration_header,
         self.registration_attachment) = self.register(app_info, new_post)
        credentials_link = self.get_link_from_header(self.registration_header)
        self.credentials = self.get_credentials(credentials_link)

        # OAuth
        id_value = self.registration_attachment['post']['id']
        oauth_auth = servers_list[0]['urls']['oauth_auth']
        code = self.authorization_request(oauth_auth, id_value)

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
            link = entity_url + rel_link
        # Discovery via HTML doc.
        else:
            soup = bs4.BeautifulSoup(response.text)
            link = soup.head.link.get('href')
        discovery_string = requests.get(link)
        return json.loads(discovery_string.text)

    # Creates an app post on the server.
    #
    # Returns the registration response header and the response attachment as dictionaries.
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
    def authorization_request(self, oauth_auth, id_value):
        payload = {'client_id': id_value}
        response = requests.get(oauth_auth, params=payload)
        location = response.history[0].headers.get('location')
        parsed_location = urlparse.urlparse(location)
        return urlparse.parse_qs(parsed_location.query)['code']
