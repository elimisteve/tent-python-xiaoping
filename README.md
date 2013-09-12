# Introduction

Xiaoping is a Python client library for [Tent](https://tent.io) v0.3. I'm writing it to get practice with the Tent protocol. Thanks to the [longears/python-tent-client](https://github.com/longears/python-tent-client) (for Tent v0.1) and [tent-client-ruby](https://github.com/tent/tent-client-ruby) repositories for serving as references.

# Status

Working but fragile. Not ready for production.

# Test Setup

Testing requires a Tent entity under your control. It currently makes changes to that entity such as creating app and status posts.

One place to create a Tent entity is [cupcake.io](https://cupcake.io/). After you've done so run:

    $ pip install -r requirements.txt
    $ cp example_config.py config.py

And set the `test_entity` variable in `config.py`.

# Run Tests

    $ python -m unittest discover xiaoping

. . . and follow the directions.

# Feedback

Criticism would be *greatly* appreciated. Email me at [ian@housejeffries.com](mailto:ian@housejeffries.com).
