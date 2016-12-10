# -*- coding: utf-8 -*-
"""Setup for yelp-dataset."""
from setuptools import setup, find_packages

requires = [
        'pillow'
        'geocoder',
        'randomdict',
        ]

setup(
        name='Speculation on Yelp-steroids'
        description='for the Yelp datasets.',
        author='Yelp',
        # url='https://github.com/Yelp/dataset-examples',
        packages=find_packages(),
        install_requires=requires,
        tests_require=requires,
        )

