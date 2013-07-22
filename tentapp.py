import json
import sys

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
        servers_list = self.discovery_response['post']['content']['servers']
        # TODO Should iterate through servers_list
        # in case there's more than one.
        new_post = servers_list[0]['urls']['new_post']
        (self.registration_header,
         self.registration_attachment) = self.register(new_post)

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
        # this is a dict
        return json.loads(discovery_string.text)

    def register(self, new_post):
        headers = {'Content-Type': ('application/vnd.tent.post.v0+json;'
                                    ' type="https://tent.io/types/app/v0#"')}
        json_file = open('registration.json').read()
        post_creation_response = requests.post(new_post, data=json_file,
                                               headers=headers)
        return str(post_creation_response.headers), post_creation_response.text
