#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
import opentargets_checkomatic as p


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(name=p.__pkgname__,
      version=p.__version__,
      description=p.__description__,
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
          'console_scripts': ['opentargets_checkomatic=opentargets_checkomatic.cli:main'],
      },
      data_files=[],
      scripts=[])
