#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='poppy-rate',
    version='0.0.7',
    packages=find_packages(),
    install_requires=['pypot', 'poppy_humanoid', 'poppy-creature'],
    include_package_data=True,
    exclude_package_data={'': ['README', '.gitignore']},
    zip_safe=False,
    author='Bumblebee',
    author_email='git@bumblebee.cc',
    url='https://github.com/bumblebeefr/poppy_rate',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
)
