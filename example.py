import os
import pickle
import sys

sys.path.append('xiaoping')
from tentapp import TentApp


###############################################################################
# Set up the app.
###############################################################################

entity_url = open('example_info/entity_url').read().rstrip()
registration_json = open('test_info/registration.json').read()
app = TentApp(entity_url, registration_json)
pickle_path = os.path.join('example_info', 'pickled_app')
if os.path.isfile(pickle_path):
    pickle_file = open(pickle_path)
    app = pickle.load(pickle_file)
else:
    app.setup()
    pickle_file = open(pickle_path, 'w')
    pickle.dump(app, pickle_file)
pickle_file.close()
