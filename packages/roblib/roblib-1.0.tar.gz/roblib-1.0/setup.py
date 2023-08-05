#!/usr/bin/env python

from distutils.core import setup

setup(name='roblib',
      version='1.0',
      description='Python Distribution Utilities',
      author='Luc Laulin',
      author_email='lucjaulin@gmail.com ',
      url='https://www.ensta-bretagne.fr/jaulin/',
      packages=['roblib'],
      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pyqt5'
      ],
     )