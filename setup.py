#!/usr/bin/python


import os
import sys

from setuptools import setup, find_packages

setup(name='strider',
      version="0.0.12",
      description='Strider builds dev VMs and bakes cloud images.',
      author='Michael DeHaan',
      author_email='michael.dehaan@gmail.com',
      url='http://github.com/mpdehaan/strider/',
      license='Apache2',
      install_requires=['boto', 'python-vagrant'],
      package_dir={ '': 'lib' },
      packages=find_packages('lib'),
      classifiers=[
      ],
      scripts=[
      ],
      data_files=[
      ],
)
