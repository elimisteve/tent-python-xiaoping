import json


class PostUtility:

    def get_posts_list(self):
        servers_list = self.discovery_response['post']['content']['servers']
        url = servers_list[0]['urls']['posts_feed']
        headers = {'Accept': 'application/vnd.tent.posts-feed.v0+json'}
        method = 'GET'
        response = self.make_request(url, method, headers=headers)
        attachment_dict = json.loads(response.text)
        return attachment_dict['posts']

    # Create a status post on the server.
    #
    # Returns the response for testing purposes.
    def post_status(self, text):
        servers_list = self.discovery_response['post']['content']['servers']
        url = servers_list[0]['urls']['new_post']
        method = 'POST'
        post_type = 'https://tent.io/types/status/v0#'
        content_type = 'application/vnd.tent.post.v0+json'
        headers = {'Content-Type': content_type + '; type="' + post_type + '"'}
        data_dict = {'type': post_type, 'content': {'text': text}}
        data = json.dumps(data_dict)
        return self.make_request(url, method, headers=headers, data=data)
