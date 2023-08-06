# coding: utf-8
import json
import os

from ubik.core import conf
from ubik.core import db

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.database import Database
from ubik.status import status

def get_stats():
	fmt = [	('Key', 'info', 25),
			('Value', 'data', 5)]
	data = [{	'info': 'Installed packages',
				'data': db.count_installed()},
			{	'info': 'Updates available',
				'data': db.count_upgrades()},
			{	'info': 'Total packages',
				'data': db.count_packages()}]

	stream_logger.info('')
	stream_logger.info(TablePrinter(fmt, data, ul='='))
	stream_logger.info('')

def get_conf():
	fmt = [('Section/Key', 'key', 25), ('Value', 'value', 50)]
	data = []
	for section in conf.sections():
		for key, value in conf.items(section):
			data.append({'key': '%s/%s' % (section, key), 'value': value})

	stream_logger.info('')
	stream_logger.info(TablePrinter(fmt, data, ul='-'))
	stream_logger.info('')

def get_view():

	if not os.path.exists(conf.get('paths', 'infos')):
		last_update = "Never"
	else:
		last_update = json.load(open(conf.get('paths', 'infos')))['last_update']

	header = """
 System : %s %s %s
 Repo   : %s/%s/%s
 Last Update : %s
""" % (	conf.get('system', 'dist').title(),
		conf.get('system', 'vers'),
		conf.get('system', 'arch'),
		conf.get('repo', 'url'),
		conf.get('repo', 'base'),
		conf.get('repo', 'branch'),
		last_update)

	fmt = [	('Name',	'name',		25),
			('Version',	'version',	25),
			('Status',	'status',	20)]
	data = []

	# Package.db	
	for name, package in db.packages.items():
		# Version output
		if package.repo_version:
			if not package.version:
				version = '[%s-%s]' % (package.repo_version, package.repo_release)
			else:
				version = '%s-%s [%s-%s]' % (	package.version, package.release,
												package.repo_version, package.repo_release)
		else:
			version = package.version + '-' + package.release

		data.append({	'name': name,
						'version': version,
						'status': status[package.status]})

	if not data:
		stream_logger.info(header)
		stream_logger.info('No package installed')
		return

	data = sorted(data, key=lambda k: k['name'])

	stream_logger.info(header)
	stream_logger.info(TablePrinter(fmt, data, ul='-'))

class TablePrinter(object):
	"Print a list of dicts as a table"
	def __init__(self, fmt, data, sep=' ', ul=None):
		"""		
		@param fmt: list of tuple(heading, key, width)
						heading: str, column label
						key: dictionary key to value to print
						width: int, column width in chars
		@param sep: string, separation between columns
		@param ul: string, character to underline column label, or None for no underlining
		"""
		self.datalist = data
		self.fmt = str(sep).join('{lb}{0}:{1}{rb}'.format(key, width, lb='{', rb='}') for heading,key,width in fmt)
		self.head = dict((key, heading) for (heading,key,width) in fmt)
		self.ul	= dict((key, str(ul)*width) for (heading,key,width) in fmt) if ul else None
		self.width = dict((key,width) for (heading,key,width) in fmt)

	def row(self, data):
		return self.fmt.format(**dict((k,str(data.get(k,''))[:w]) for (k,w) in self.width.iteritems()))

	def __str__(self):
		_r = self.row
		res = [_r(data) for data in self.datalist]
		res.insert(0, _r(self.head))
		if self.ul:
			res.insert(1, _r(self.ul))
		return '\n'.join(res)
