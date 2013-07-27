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
