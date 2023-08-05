import sys
from setuptools import setup, find_packages

REQUIRED_PACKAGES = ['numpy', 'torch']

setup(
    name='compyt',
    version='1.6',
    packages=['compyt'],
    author=['Michael Kellman'],
    author_email='michael.kellman@ucsf.edu',
    license='BSD',
    long_description=open('README.md').read(),
)