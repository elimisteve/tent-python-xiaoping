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
