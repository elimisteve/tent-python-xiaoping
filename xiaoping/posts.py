import json


class Post:

    def __init__(self, post_type, content):
        self.post_type = post_type
        self.content = content


class AppPost:

    def __init__(self, app_name, read=None, write=None,
                 url='https://app.example.com',
                 redirect_url='https://app.example.com'):
        self.post_type = 'https://tent.io/types/app/v0#'
        self.content = {'name': app_name,
                        'scopes': ['permissions'],
                        'url': url,
                        'types': {'read': read,
                                  'write': write},
                        'redirect_uri': redirect_url}


class PostUtility:

    def create_post(self, post):
        url = self.get_server()['urls']['new_post']
        content_type = 'application/vnd.tent.post.v0+json'
        headers = {'Content-Type': (content_type + '; type="' +
                                    post.post_type + '"')}
        data_dict = {'type': post.post_type, 'content': post.content}
        data = json.dumps(data_dict)
        return self.make_request(url, 'POST', headers, data)

    def get_posts_list(self):
        url = self.get_server()['urls']['posts_feed']
        headers = {'Accept': 'application/vnd.tent.posts-feed.v0+json'}
        method = 'GET'
        response = self.make_request(url, method, headers)
        attachment_dict = json.loads(response.text)
        return attachment_dict['posts']
