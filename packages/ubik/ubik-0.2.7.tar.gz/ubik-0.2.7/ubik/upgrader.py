# coding: utf-8
from ubik.core import db
from ubik.core import conf

from ubik.logger import stream_logger
from ubik.logger import logger

from ubik.package import Package
from ubik.downloader import get_package
from ubik.tools import checkmd5
from ubik.exceptions import UpgraderException

class Upgrader(object):
	def __init__(self):
		self.packages = []

	def feed(self, packages):
		if not isinstance(packages, list):
			packages = [packages]

		for package in packages:
			if not isinstance(package, Package):
				packages += db.get(package)
				del packages[packages.index(package)]

		for package in packages:
			if package not in self.packages:
				if package.status in ['1','2']:
					self.packages.append(package)
				elif package.status == '0':
					stream_logger.info('    - %s already up-to-date' % package.name)
				elif package.status == '10':
					stream_logger.info('    - %s not installed' % package.name)
				elif package.status in ['11','12']:
					stream_logger.info('    - %s can not be downgraded' % package.name)
				else:
					stream_logger.info('    - %s can not be updated' % package.name)

	def download(self):
		stream_logger.info(' :: Download')
		for package in self.packages:
			logger.info('Download %s' % package.name)
			get_package(package)
			if not checkmd5(package):
				logger.info('%s md5 invalid' % package.name)
				stream_logger.info('   | Md5 invalid, package corrumpt')	
				raise UpgraderException('Invalid Md5')

	def upgrade(self, ignore_errors=False):
		if not self.packages:
			raise UpgraderException('Nothing to upgrade')
		stream_logger.info(' :: Upgrade')	
		for package in self.packages:
			package.upgrade(ignore_errors)
			stream_logger.info('      | Update database')
			package.status = "0"
			package.version = package.repo_version
			package.release = package.repo_release
			package.repo_version = ''
			package.repo_release = ''
			db.add(package)
