# coding: utf-8
from ubik.core import db
from ubik.core import conf

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.package import Package
from ubik.downloader import get_package
from ubik.tools import cached
from ubik.tools import checkmd5
from ubik.exceptions import InstallerException

class Installer(object):
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
				if package.status in ['10']:
					self.packages.append(package)
				else:
					stream_logger.info('    - %s already installed' % package.name)
			else:
				logger.debug('%s ignored' % package.name)

	def resolve(self, package):
		self.package = package
		self.tree = [self.package]
		self.resolved = []
		logger.debug("Resolv deps for '%s':" % package.name)
		self.deps_resolve(self.package, self.resolved, [])

	def deps_resolve(self, package, resolved, unresolved, level=0):
		logger.debug("[%s] %s: %s" % (level, package.name ,package.requires))
		self.unresolved = unresolved
		self.unresolved.append(package)
		for dep in db.get(package.requires, regexp = False):
			if dep.name not in [_dep.name for _dep in self.resolved]:
				if dep.name in [_dep.name for _dep in self.unresolved]:
					raise InstallerException('Circular reference detected: %s -> %s' % (package.name, dep.name))
				self.deps_resolve(dep, self.resolved, self.unresolved, level+1)
		self.resolved.append(package)
		self.unresolved.remove(package)

	def download(self):
		stream_logger.info(' :: Download')
		for package in self.packages:
			logger.info('Download %s' % package.name)
			# Not cached
			if not cached(package):
				logger.info('%s not cached' % package.name)
				get_package(package)
				# Invalid Md5
				if not checkmd5(package):
					logger.info('%s md5 invalid' % package.name)
					stream_logger.info('   | Md5 invalid, package corrumpt')
					raise InstallerException('Invalid Md5')
			# Cached
			else:
				logger.info('%s already in cache' % package.name)
				# Invalid Md5, redownload
				if not checkmd5(package):
					logger.info('%s cache package md5 invalid' % package.name)
					get_package(package)
					if not checkmd5(package):
						logger.info('%s md5 invalid' % package.name)
						stream_logger.info('   | Md5 invalid, package corrumpt')
						raise InstallerException('Invalid Md5')
				else:
					stream_logger.info('    | %s already in cache' % package.name)

	def install(self, ignore_errors=False):
		if not self.packages:
			raise InstallerException('Nothing to install')
		stream_logger.info(' :: Install')
		for package in self.packages:
			package.install(ignore_errors=ignore_errors)
			stream_logger.info('      | Update database')
			package.status = "0"
			package.version = package.repo_version
			package.release = package.repo_release
			package.repo_version = ''
			package.repo_release = ''
			db.add(package)
