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
    VERSIONFILE = 'fotografering'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

setup(
	name='Fotografering',
	version=get_version(),
	description='Fotografering, linkify and beautify your photos.',
	long_description=open('README.rst').read(),
	license=open('LICENSE').read(),
	author='toxinu',
	author_email='toxinu@gmail.com',
	url='https://github.com/toxinu/fotografering',
	keywords='## Set keywords',
	scripts=['fotografering'],
	install_requires=['docopt', 'requests'],
	classifiers=(
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7')
)
