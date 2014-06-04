import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "passout",
    version = "0.1",
    author = "Mike Culbertson",
    author_email = "mculbertson@pivotal.io",
    description = ("Comically simplistic utility to help keep usernames and passwords out of code"),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://pivotal.io",
    packages=['passout'],
    long_description=read('Readme.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
    ],
)
