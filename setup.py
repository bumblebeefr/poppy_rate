#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='poppy_rate',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['pypot', 'poppy_humanoid'],
    zip_safe=False,
    author='Bumblebee',
    author_email='git@bumblebee.cc',
    url='https://github.com/bumblebeefr/poppy_rate',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
)
