#!/usr/bin/env python

from setuptools import setup
from magictime import version

setup(name='Magictime',
      version=version,
      description='Simple time object',
      author='Oleg Makarov',
      author_email='oleg@ledorub.org',
      packages=['magictime'],
      zip_safe=False,
      install_requires=[
        'dateutil.parser',
        'datetime',
        'time',
      ])