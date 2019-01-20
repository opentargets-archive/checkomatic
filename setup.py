#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
import opentargets_checkomatic as p
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

# read the contents of your README file
# https://packaging.python.org/guides/making-a-pypi-friendly-readme/
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name=p.__pkgname__,
      version=p.__version__,
      description=p.__description__,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=p.__author__,
      author_email=p.__author__,
      maintainer='Miguel Carmona',
      maintainer_email='carmona@ebi.ac.uk',
      url=p.__homepage__,
      packages=['opentargets_checkomatic'],
      license=p.__license__,
      keywords=['opentargets', 'bioinformatics', 'python2'],
      platforms=['any'],
      install_requires=requirements,
      dependency_links=[],
      include_package_data=True,
      entry_points={
          'console_scripts': ['opentargets_checkomatic=opentargets_checkomatic.cli:cli'],
      },
      data_files=[],
      scripts=[])
