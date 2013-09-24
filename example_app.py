import datetime

import config
from xiaoping.tentapp import TentApp
from xiaoping.posts import AppPost, Post


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


# 1. Run the following if you haven't already:
#    $ pip install -r requirements.txt
#    $ cp example_config.py config.py

# 2. Set `EXAMPLE_APP_ENTITY` in `config.py`.

# 3. Run the app:
#    $ python example_app.py


###############################################################################
# Setup
###############################################################################


app_post = AppPost('Xiaoping Example App',
                   write=['https://tent.io/types/status/v0'])
app = TentApp(config.EXAMPLE_APP_ENTITY, app_post)
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


status_type = 'https://tent.io/types/status/v0#'
status_post = Post(status_type, {'text': raw_input('Type your status post: ')})
app.create_post(status_post)

for i in app.get_posts_list({'types': status_type, 'limit': 5}):
    text = i['content']['text']

    unix_time_in_s = i['published_at']/1000.0
    published_at = datetime.datetime.fromtimestamp(unix_time_in_s)
    formatted_time = published_at.strftime('%Y-%m-%d %H:%M:%S')

    print ('======================================='
           '=======================================')
    print 'Text:         ' + text
    print 'Published at: ' + formatted_time
    print ''
