#!/usr/bin/env python

from os.path import abspath, dirname, join

from src.RequestsProLibrary import VERSION
import setuptools

try:
    from setuptools import setup
except ImportError as error:
    from distutils.core import setup

version_file = join(dirname(abspath(__file__)), 'src', 'RequestsProLibrary', 'version.py')

with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

DESCRIPTION = """
Robot Framework keyword library wrapper around the HTTP client library requests.
"""[1:-1]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(name='robotframework-requestspro',
      version=VERSION,
      description='Robot Framework keyword library wrapper around requests',
      long_description=DESCRIPTION,
      author='Sridhar VP',
      author_email='sridharvpmca@gmail.com',
      url='https://github.com/sridharvpmca/robotframework-requestspro',
      license='MIT',
      keywords='robotframework testing test automation http client requests',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=['RequestsProLibrary'],
      package_data={'RequestsProLibrary': ['tests/*.txt']},
      install_requires=[
          'pandas',
          'requests',
          'robotframework',
          'robotframework-requests',
      ],
      )

""" From now on use this approach

python setup.py sdist upload
git tag -a 1.2.3 -m 'version 1.2.3'
git push --tags"""
