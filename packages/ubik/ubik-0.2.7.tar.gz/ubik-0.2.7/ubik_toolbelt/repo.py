# coding: utf-8
from __future__ import with_statement

import os
import sys
import tarfile
import subprocess
import hashlib
import shutil

try:
    import json
except ImportError:
    import simplejson as json 

from urlparse import urlparse

from ubik_toolbelt.logger import stream_logger

packages_list = 'Packages.list'
packages_json = 'Packages.json'

def create(repo_name):

	if os.path.exists(repo_name) and repo_name != ".":
		stream_logger.info(' :: Dir already exist')
		sys.exit(1)

	stream_logger.info(' :: Create repository structure')
	if repo_name != '.':
		os.makedirs(repo_name)
		os.chdir(repo_name)
	open('.repo_root', 'w').close

	stream_logger.info(' :: Create default "stable" branch and two examples')
	os.makedirs('stable')
	os.makedirs('stable/noarch/nodist/novers')
	os.makedirs('stable/x86_64/debian/6')

def get_md5(path):
	fh = open(path, 'rb')
	m = hashlib.md5()
	while True:
		data = fh.read(8192)
		if not data:
			break
		m.update(data)
	return m.hexdigest()

def unarchiver(prefix, path, name):
	src = "%s/%s.tar" % (path, name)
	dst = "%s/%s" % (prefix, path)

	# Open tarfile
	tar = tarfile.open(src)
	if tarfile.is_tarfile(src):
		tar.extractall(dst)
	else:
		raise Exception('Archive invalid (not a tarfile)')

def get_package_infos(prefix, path, name):
	infos = {}

	sys.path.append(os.path.join(path, name))
	control_module =  __import__('control')
	sys.path.remove(os.path.join(path, name))
	sys.modules.pop('control')
	control = control_module.Package()

	infos['name'] = control.name
	infos['version'] = control.version
	infos['release'] = control.release
	infos['description'] = control.description
	infos['requires'] = control.requires

	infos['arch'] = path.split('/')[1]
	infos['dist'] = path.split('/')[2]
	infos['vers'] = path.split('/')[3]

	if control.arch:
		if control.arch != infos['arch']:
			stream_logger.info('Bad arch (ignore it)')
			return False

		if control.dist:
			if control.dist != infos['dist']:
				stream_logger.info('Bad dist (ignore it)')
				return False

			if control.vers:
				if control.vers != infos['vers']:
					stream_logger.info('Bad vers (ignore it)')
					return False

	infos['md5'] = get_md5(path + '/' + name + '.tar')
	return infos

def write_packages_json(infos, branch):
	path = branch + '/' + packages_json
	json.dump(infos, open(path, 'w'))

def clean(path, name):
	shutil.rmtree('%s/%s' % (path, name))

def generate(branches=False, old_format=False, tmp_dir=False):
	if not os.path.exists('.repo_root'):
		stream_logger.info(' :: Need to be at repository root')
		sys.exit(1)

	if not tmp_dir:
		prefix = os.getcwd()
	else:
		prefix = tmp_dir
		if not os.path.exists(prefix):
			os.makedirs(prefix)

	if not branches:
		branches = filter(os.path.isdir, os.listdir('.'))
	elif not isinstance(branches, list):
		branches = [branches]

	for branch in branches:
		if branch[0] == ".":
			continue
		_json = []

		for (path, dirs, files) in os.walk(branch):
			if len(path.split('/')) == 1:
				stream_logger.info(' + %s' % path.split('/')[0])
			elif len(path.split('/')) == 2:
				stream_logger.info('   |_ %s' % path.split('/')[1])
			elif len(path.split('/')) == 3:
				stream_logger.info('     |_ %s' % path.split('/')[2])
			elif len(path.split('/')) == 4:
				stream_logger.info('       |_ %s' % path.split('/')[3])
				for package in files:
					if package[-4:] != '.tar':
						stream_logger.info('         |_ %s (ignored)' % package[:-4])
						continue
					package = package[:-4]
					stream_logger.info('         |_ %s' % package)
					unarchiver(prefix, path, package)
					_json.append(get_package_infos(prefix, path, package))
					clean("%s/%s" % (prefix, path), package)
		write_packages_json(_json, branch)

	if tmp_dir:
		shutil.rmtree(prefix)
