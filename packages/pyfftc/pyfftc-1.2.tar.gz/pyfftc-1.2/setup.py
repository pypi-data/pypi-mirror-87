import sys
from setuptools import setup, find_packages

setup(
    name='pyfftc',
    version='1.2',
    packages=['pyfftc'],
    author=['Michael Kellman'],
    author_email='michael.kellman@ucsf.edu',
    license='BSD',
    long_description=open('README.md').read(),
    install_requires=['torch>=1.7.0']
)