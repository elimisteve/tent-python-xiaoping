# Introduction

Xiaoping is a Python client library for [Tent](https://tent.io) v0.3. I'm writing it to get practice with the Tent protocol. Thanks to the [longears/python-tent-client](https://github.com/longears/python-tent-client) (for Tent v0.1) and [tent-client-ruby](https://github.com/tent/tent-client-ruby) repositories for serving as references.

# Status

Very little works so far. What does work only works on the alpha server because it skips an authentication step.

# Setup

    $ pip install -r requirements.txt

# Test Setup

Testing requires an entity under your control (here `https://example.com/`). It currently makes changes to that entity such as creating app posts.

    $ mkdir test_info
    $ echo https://example.com/ > test_info/entity_url
    $ cp sample_registration.json test_info/registration.json

Change "redirect_uri" in `registration.json` to a URL under your control.

# Run Tests

    $ python tests/tentapp_test.py
    $ python tests/pyhawk_test.py

# Feedback

Criticism would be *greatly* appreciated. Email me at [ian@housejeffries.com](mailto:ian@housejeffries.com).
