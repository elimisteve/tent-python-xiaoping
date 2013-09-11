#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='xiaoping',
    version='0.1.0',
    author='Ian Grant Jeffries',
    author_email='ian@housejeffries.com',
    url='https://github.com/seagreen/tent-python-xiaoping',
    license=open('MIT-LICENSE.txt').read(),
    packages=['xiaoping'],
    package_dir={'requests': 'requests'}
)
