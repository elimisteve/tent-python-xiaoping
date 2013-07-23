# Introduction

Xiaoping is a Python client library for [Tent](https://tent.io) v0.3. I'm writing it to get practice with the Tent protocol. Thanks to the [longears/python-tent-client](https://github.com/longears/python-tent-client) (for Tent v0.1) and [tent-client-ruby](https://github.com/tent/tent-client-ruby) repositories for serving as references.

# Setup

1. Run the following commands:
    ```
    $ pip install -r requirements.txt
    $ cp sample_registration.json registration.json
    ```

2. Change "redirect_uri" in `registration.json` to a URL under your control.

# Testing

    $ python tentapp_test.py <your_entity_url>

# Feedback

Criticism would be *greatly* appreciated. Email me at [ian@housejeffries.com](mailto:ian@housejeffries.com).
