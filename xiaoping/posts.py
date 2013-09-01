import json


class PostUtility:

    def get_posts_list(self):
        url = self.get_server()['urls']['posts_feed']
        headers = {'Accept': 'application/vnd.tent.posts-feed.v0+json'}
        method = 'GET'
        response = self.make_request(url, method, headers)
        attachment_dict = json.loads(response.text)
        return attachment_dict['posts']

    # Create a status post on the server.
    #
    # Returns the response.
    def post_status(self, text, mentions_list=[]):
        url = self.get_server()['urls']['new_post']
        method = 'POST'
        post_type = 'https://tent.io/types/status/v0#'
        content_type = 'application/vnd.tent.post.v0+json'
        headers = {'Content-Type': content_type + '; type="' + post_type + '"'}
        mentions = []
        for entity in mentions_list:
            mentions.append({'entity': entity})
        data_dict = {'type': post_type,
                     'content': {'text': text},
                     'mentions': mentions}
        data = json.dumps(data_dict)
        return self.make_request(url, method, headers, data)
