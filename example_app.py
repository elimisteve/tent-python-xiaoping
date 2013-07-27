import datetime
import os
import pickle
import sys

sys.path.append('xiaoping')
from tentapp import TentApp


###############################################################################
# About
###############################################################################


# This app lets you create a status post and then prints your last five
# status posts.

# The instructions in "Make preparations" must be carried out before it
# can be run for the first time. After that the app will save its state
# in the file: `data_for_example/pickled_app`.


###############################################################################
# Make preparations
###############################################################################


# 1. Run the following:
#    $ mkdir data_for_testing
#    $ echo https://my-entity.example.com/ > data_for_testing/entity_url
#    $ cp sample_registration.json data_for_testing/registration.json

# 2. Change "redirect_uri" in `registration.json` to a URL under your control.

# 3. Run the app:
#    $ python example_app.py


###############################################################################
# Setup
###############################################################################


pickle_path = os.path.join('data_for_example', 'pickled_app')
if os.path.isfile(pickle_path):
    pickle_file = open(pickle_path)
    app = pickle.load(pickle_file)
else:
    entity_path = os.path.join('data_for_example', 'entity_url')
    entity_url = open(entity_path).read().rstrip()
    registration_path = os.path.join('data_for_example', 'registration.json')
    registration_json = open(registration_path).read()
    app = TentApp(entity_url, registration_json)
    app.setup()
    pickle_file = open(pickle_path, 'w')
    pickle.dump(app, pickle_file)
pickle_file.close()


###############################################################################
# In use
###############################################################################


app.post_status(raw_input('Type your status post: '))

posts_list = app.get_posts_list()
status_type = 'https://tent.io/types/status/v0#'
status_posts = [i for i in posts_list if i['type'] == status_type]

for i in status_posts[:5]:
    text = i['content']['text']
    unix_time_in_s = i['published_at']/1000.0
    published_at = datetime.datetime.fromtimestamp(unix_time_in_s)
    pretty_print_time = published_at.strftime('%Y-%m-%d %H:%M:%S')

    print ('======================================='
           '=======================================')
    print 'Text:         ' + text
    print 'Published at: ' + pretty_print_time
    print ''
