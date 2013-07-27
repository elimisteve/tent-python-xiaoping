from registration import PreRegistration


class TentApp(PreRegistration):

    def __init__(self, entity_url, registration_json):

        # Initial info to set up the app.
        self.entity_url = entity_url
        self.app_info = registration_json

        # These will get filled in as we go through registration.
        self.discovery_response = None
        self.registration_header = None
        self.registration_attachment = None
        self.credentials = None
        self.token_header = None
        self.token_attachment = None

        self.id_value = None
        self.hawk_key = None
        self.app_id = None

    def setup(self):

        ### Discovery
        self.discovery_response = self.discover(self.entity_url)

        ### Registration
        servers_list = self.discovery_response['post']['content']['servers']
        # TODO Should iterate through servers_list
        # in case there's more than one.
        new_post = servers_list[0]['urls']['new_post']
        (self.registration_header,
         self.registration_attachment) = self.register(self.app_info, new_post)
        credentials_link = self.get_link_from_header(self.registration_header)
        self.credentials = self.get_credentials(credentials_link)

        ### OAuth
        temp_id = self.registration_attachment['post']['mentions'][0]['post']
        temp_app_id = self.registration_attachment['post']['id']
        oauth_auth = servers_list[0]['urls']['oauth_auth']
        code = self.authorization_request(oauth_auth, temp_app_id)
        oauth_token = servers_list[0]['urls']['oauth_token']
        hawk_key = self.credentials['post']['content']['hawk_key']
        hawk_key = hawk_key.encode('ascii')
        # There's got to be a less ugly way to fit this in 80 lines.
        (self.token_header,
         self.token_attachment) = self.access_token_request(oauth_token, code,
                                                            temp_id, hawk_key,
                                                            temp_app_id)
        self.id_value = self.token_attachment['access_token']
        self.hawk_key = self.token_attachment['hawk_key'].encode('ascii')
        self.app_id = self.registration_attachment['post']['id']
