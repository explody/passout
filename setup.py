import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="passout",
    version="0.4",
    author="Mike Culbertson",
    author_email="mikelcu@gmail.com",
    description=(
        "Small, simplistic utility to help keep usernames and passwords out of code"),
    license="BSD",
    keywords="password security credentials",
    packages=['passout'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
    ],
)
