#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup
import checkomatic as p


setup(name=p.__pkgname__, version=p.__version__,
      description=p.__description__, author=p.__author__,
      author_email=p.__author__,
      maintainer='mkarmona',
      maintainer_email='carmona@ebi.ac.uk',
      url=p.__homepage__,
      packages=['checkomatic'],
      license=p.__license__,
      platforms=['any'],
      install_requires=[],
      dependency_links=[],
      include_package_data=True,
      entry_points={
          'console_scripts': ['checkomatic=checkomatic.cli:main'],
      },
      data_files=[],
      scripts=[])
