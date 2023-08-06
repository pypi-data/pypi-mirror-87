#!/usr/bin/env python
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(author='David Black',
      author_email='dblack@atlassian.com',
      url='https://bitbucket.org/db_atlass/python-junit-xml-output-module',
      packages=find_packages(),
      test_suite='junit_xml_output.test',
      platforms=['any'],
      setup_requires=['pbr<=6.0.0'],
      pbr=True,
      )
