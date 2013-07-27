import json

import requests
import hawk


class PostUtility:

    def get_posts_list(self):
        servers_list = self.discovery_response['post']['content']['servers']
        url = servers_list[0]['urls']['posts_feed']
        credentials = {'id': self.id_value,
                       'key': self.hawk_key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'app': self.app_id,
                   'ext': ''}
        header = hawk.client.header(url, 'GET', options=options)['field']
        headers = {'Accept': 'application/vnd.tent.posts-feed.v0+json',
                   'Authorization': header}
        response = requests.get(url, headers=headers)
        attachment_dict = json.loads(response.text)
        return attachment_dict['posts']

    # Create a status post on the server.
    #
    # Returns the response for testing purposes.
    def post_status(self, text):
        servers_list = self.discovery_response['post']['content']['servers']
        url = servers_list[0]['urls']['new_post']
        content_type = 'application/vnd.tent.post.v0+json'
        status_type = 'https://tent.io/types/status/v0#'
        data_dict = {'type': status_type,
                     'content': {'text': text}}
        data = json.dumps(data_dict)
        credentials = {'id': self.id_value,
                       'key': self.hawk_key,
                       'algorithm': 'sha256'}
        options = {'credentials': credentials,
                   'payload': data,
                   'contentType': content_type,
                   'app': self.app_id,
                   'ext': '',
                   'dlg': ''}
        header = hawk.client.header(url, 'POST', options=options)['field']
        headers = {'Authorization': header,
                   'Content-Type': content_type + ';'
                   + ' type="' + status_type + '"'}
        return requests.post(url, data=data, headers=headers)
