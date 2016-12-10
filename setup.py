# -*- coding: utf-8 -*-
"""Setup for yelp-dataset."""
from setuptools import setup, find_packages

requires = [
        'pillow',
        'geocoder',
        'randomdict',
        ]

setup(
        name='Speculation on Yelp-steroids',
        description='for the Yelp datasets.',
        author='Yelp',
        url='git@github.com:WesCoomber/582Wcoomber3.git',
        packages=find_packages(),
        install_requires=requires,
        tests_require=requires,
        )

