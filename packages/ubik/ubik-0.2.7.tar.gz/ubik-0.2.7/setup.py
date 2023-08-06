#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.version < '3':
  import codecs
  def u(x):
    return codecs.unicode_escape_decode(x)[0]
else:
  def u(x):
    return x

def get_version():
    VERSIONFILE = 'ubik/__init__.py'
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

setup(
    name='ubik',
    version=get_version(),
    description=u('Minimal and elegant packages manager'),
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author=u('toxinu'),
    author_email=u('toxinu@gmail.com'),
    url='https://github.com/toxinu/ubik/',
    keywords='ubik package linux unix',
    packages=['ubik','ubik_toolbelt','ubik_toolbelt.contrib'],
    scripts=['scripts/ubik', 'scripts/echo_ubik_conf', 'scripts/ubik-package', 'scripts/ubik-repo', 'scripts/ubik-web'],
    install_requires=['progressbar==2.3', 'requests==1.1.0', 'docopt==0.5.0', 'isit==0.3.5'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'],
)
