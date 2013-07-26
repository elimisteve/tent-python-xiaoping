import os
import pickle
import sys

sys.path.append('xiaoping')
from tentapp import TentApp


###############################################################################
# Set up the app.
###############################################################################

entity_url = open('data_for_example/entity_url').read().rstrip()
registration_json = open('data_for_example/registration.json').read()
app = TentApp(entity_url, registration_json)
pickle_path = os.path.join('data_for_example', 'pickled_app')
if os.path.isfile(pickle_path):
    pickle_file = open(pickle_path)
    app = pickle.load(pickle_file)
else:
    app.setup()
    pickle_file = open(pickle_path, 'w')
    pickle.dump(app, pickle_file)
pickle_file.close()

###############################################################################
# interact with posts.
###############################################################################



