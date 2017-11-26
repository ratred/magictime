#!/usr/bin/env python

from setuptools import setup
from magictime import version

setup(name='magictime',
      version=version,
      description='Simple time object',
      author='Oleg',
      author_email='oleg@ledorub.org',
      packages=['magictime'],
      zip_safe=False,
      install_requires=[
        'dateutil.parser',
        'datetime',
        'time',
      ])