import datetime
import os
import sys

project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_path, 'xiaoping'))
from tentapp import TentApp


###############################################################################
# About
###############################################################################


# This app lets you create a status post and then prints your last five
# status posts.
#
# You must already have a Tent server set up for it to work. One place that
# can be done is: https://cupcake.io/


###############################################################################
# Make preparations
###############################################################################


# 1. Run the following:
#    $ mkdir data_for_testing
#    $ echo https://my-entity.example.com/ > data_for_example/entity_url
#    $ cp sample_registration.json data_for_example/registration.json

# 2. Change "redirect_uri" in `registration.json` to a URL under your control.

# 3. Run the app:
#    $ python example_app.py


###############################################################################
# Setup
###############################################################################


entity_path = os.path.join(project_path, 'data_for_example', 'entity_url')
info_path = os.path.join(project_path, 'data_for_example', 'registration.json')

entity_url = open(entity_path).read().rstrip()
registration_json = open(info_path).read()
app = TentApp(entity_url, registration_json)
go_to_me = app.start_setup()
print 'Now you need to go to:'
print ''
print go_to_me
print ''
print 'and approve the app.'
print "After doing so you'll be redirected to a new page."
print "Get the code parameter from that page's URL and enter it here."
code = raw_input('> ')
app.finish_setup(code)
# A real app would store app.app_id, app.id_value, and app.hawk_key
# at this point.


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
