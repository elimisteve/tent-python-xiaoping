#!/usr/bin/env python

from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_reqs = parse_requirements("requirements.txt")
requirements = [str(i.req) for i in install_reqs]
import ipdb; ipdb.set_trace() # ------------------------ #

setup(
    name='xiaoping',
    version='0.1.0',
    author='Ian Grant Jeffries',
    author_email='ian@housejeffries.com',
    url='https://github.com/seagreen/tent-python-xiaoping',
    license=open('MIT-LICENSE.txt').read(),
    packages=['xiaoping'],
    package_dir={'requests': 'requests'},
    install_requires=requirements
)
