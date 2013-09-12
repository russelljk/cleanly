#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='cleanly',
      version='0.1',
      description="A Django HTML cleanup/sanitizer based on html5lib.",
      author='Russell Kyle',
      author_email='russell.j.kyle@gmail.com',
      url='http://russellkyle.com/django-cleanly/',
      download_url='https://github.com/russelljk/cleanly/archive/master.zip',
      packages=['cleanly'],
      include_package_data=True,
      install_requires = ['html5lib'],
      keywords=['HTML', 'HTML5', 'Django', 'XSS']
)
