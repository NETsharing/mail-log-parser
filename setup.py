import os
from setuptools import setup, find_packages


setup(
    name='mail log parser',
    version='1.0',
    author='Piterskikh S A',
    utl='https://github.com/piterskikhsa/mail-log-parser',
    packages=find_packages(),
    description='Parse the mail server log and collect mail statistics.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)