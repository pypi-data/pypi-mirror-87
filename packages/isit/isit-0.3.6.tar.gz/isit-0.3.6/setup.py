#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup


def get_version():
    VERSIONFILE = 'isit.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return u(mo.group(1))
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

if sys.version < '3':
  import codecs
  def u(x):
    return codecs.unicode_escape_decode(x)[0]
else:
  def u(x):
    return x

setup(
	name='isit',
	version=get_version(),
	description='Environment runtime detection (Python,Linux,Distribution,etc...)',
	long_description=open('README.rst').read(),
	author=u('toxinu'),
	author_email='toxinu@gmail.com',
	url='https://github.com/toxinu/isit',
	keywords='python linux env variable windows arch distribution',
	py_modules=['isit'],
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.4',
		'Programming Language :: Python :: 2.5',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3']
)
