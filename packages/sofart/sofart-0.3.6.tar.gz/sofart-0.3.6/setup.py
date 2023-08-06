#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

def get_version():
    VERSIONFILE = 'sofart/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

if sys.version < '3':
  import codecs
  def u(x):
    return codecs.unicode_escape_decode(x)[0]
else:
  def u(x):
    return x

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

setup(
	name=u('sofart'),
	version=get_version(),
	description=u('Python in-memory embedded and non-relationnal database'),
	long_description=open('README.rst').read(),
	license=open("LICENSE").read(),
	author=u("toxinu"),
	author_email=u("toxinu@gmail.com"),
	packages = ['sofart', 'sofart.serializers'],
	install_requires = ['isit'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
    ]
)
