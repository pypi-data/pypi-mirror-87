# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  setup_requires=['git-versiointi>=1.5rc4'],
  name='django-yleisavain',
  description='Työkaluja yleisiin vierasavaimiin liittyvien kyselyjen optimointiin',
  url='https://github.com/an7oine/django-yleisavain.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@pispalanit.fi',
  packages=find_packages(),
)
