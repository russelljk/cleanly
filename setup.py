#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='cleanly',
      version='0.1',
      description="A Django HTML cleanup/sanitizer based on html5lib.",
      author='Russell Kyle',
      author_email='russell.j.kyle@gmail.com',
      url='http://russellkyle.com/django-cleanly/',
      download_url='https://github.com/russelljk/cleanly/archive/master.zip',
      packages=find_packages(),
      include_package_data=True,
      install_requires = ['html5lib>=0.9'],
      zip_safe = False,
      keywords=['HTML', 'HTML5', 'Django', 'XSS']
)
