#!/usr/bin/env python
from distutils.core import setup

setup(
    name='poppy_rate',
    version='0.0.1',
    author='Bumblebee',
    author_email='git@bumblebee.cc',
    py_modules=['poppy_rate'],
    install_requires=['pypot', 'poppy_humanoid', 'zerorpc']
)
