# coding: utf-8
import os
import sys
import re
import json
import time

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.core import conf
from ubik.package import Package

from ubik.downloader import get_database
from ubik.exceptions import DatabaseException

class Database(object):
    def __init__(self, content=None, file_path=None):
        self.content = content
        self.file_path = file_path

        if not self.content and self.file_path:
            self.content = json.load(open(self.file_path))

        self.parse()

    def sync(self):
        self.load()
        stream_logger.info('   | Retrieving %s/%s/%s/Packages.json' % (
                        conf.get('repo', 'url'),
                        conf.get('repo', 'base'),
                        conf.get('repo', 'branch')))
        db_remote = Database(content=get_database())

        for package in db_remote.packages.values():
            # Check installed
            if package.name not in self.packages.keys():
                package.status = '10'
                self.packages[package.name] = package
            elif self.packages[package.name].status == '10':
                package.status = '10'
            # Check version
            elif package.version > self.packages[package.name].version:
                package.status = '1'
            elif package.version < self.packages[package.name].version:
                package.status = '11'
            # Check release
            elif package.release > self.packages[package.name].release:
                package.status = '2'
            elif package.release < self.packages[package.name].release:
                package.status = '12'
            # Up-to-date
            else:
                package.status = '0'

            if package.status in ['1','2','11','12']:
                package.repo_version = package.version
                package.repo_release = package.release
                package.version = self.packages[package.name].version
                package.release = self.packages[package.name].release
            elif package.status in ['10']:
                package.repo_version = package.version
                package.repo_release = package.release
                package.version = ''
                package.release = ''
            else:
                package.repo_versions = ''
                package.repo_release = ''

            self.packages[package.name] = package

        for package in self.packages.values():
            if package.name not in db_remote.packages.keys():
                if package.status in ['10']:
                    del self.packages[package.name]

        # Save databases
        self.save()

        # Save informations
        if not os.path.exists(conf.get('paths', 'infos')):
            open(conf.get('paths', 'infos'), 'w').close()

        infos = json.dump(
            {'last_update': time.ctime()},
        open(conf.get('paths', 'infos'), 'w'))

    def get(self, packages, regexp=True):
        self.load()
        if not isinstance(packages, list):
            packages = [packages]

        result = []
        for package in packages:
            if regexp:
                for key,value in self.packages.items():
                    if package[-1] != '*' and len(package) > 1:
                        pattern = re.compile(r'%s$' % package)
                    elif package[-1] == '*':
                        pattern = re.compile(package[:-1])
                    else:
                        pattern = re.compile(package)
                    if pattern.search(key):
                        result.append(value)
            else:
                try:
                    result.append(self.packages[package])
                except:
                    raise DatabaseException('Package %s not available' % package)

        return result

    def check_system(self, package):
        if package.arch != conf.get('system', 'arch'):
            if package.arch != "noarch":
                return False
        if package.dist != conf.get('system', 'dist'):
            if package.dist != "nodist":
                return False
        if package.vers != conf.get('system', 'vers'):
            if package.vers != "novers":
                return False
        return True

    def check_packages(self, p, o):
        # p is new package
        # o is old package
        if o.arch == 'noarch' and o.dist == 'nodist' and o.vers == 'novers':
            return False
        return True

    def parse(self):
        packages = {}
        for package in self.content:
            name = package['name']
            p = Package(name)
            p.fill(**package)

            if not self.check_system(p):
                continue

            if packages.get(name, False):
                if not self.check_packages(p, packages[name]):
                    continue
            packages[package['name']] = p
        self.packages = packages

    def add(self, package):
        self.load()
        if not isinstance(package, Package):
            raise DatabaseException('Package must be Package object')
        self.packages[package.name] = package
        self.save()

    def delete(self, package):
        self.load()
        if not isinstance(package, Package):
            package_name = package
        else:
            package_name = package.name
        try:
            del self.packages[package_name]
        except:
            pass
        self.save()

    def load(self):
        self.save()
        self.content = json.load(open(self.file_path))
        self.parse()

    def save(self):
        open(self.file_path, 'w').close()
        new_json = []
        for package in self.packages.values():
            _package = {'name': package.name,
                        'version': package.version,
                        'release': package.release,
                        'status': package.status,
                        'requires': package.requires,
                        'md5': package.md5,
                        'arch': package.arch,
                        'dist': package.dist,
                        'vers': package.vers,
                        'repo_version': package.repo_version,
                        'repo_release': package.repo_release}
            new_json.append(_package)

        json.dump(new_json, open(self.file_path, 'w'))

    def get_upgrades(self):
        res = []
        for package in self.packages.values():
            if package.status in ['1','2']:
                res.append(package)
        return res

    def count_upgrades(self):
        res = 0
        for package in self.packages.values():
            if package.status in ['1','2']:
                res += 1
        return res

    def get_installed(self):
        res = []
        for package in self.packages.values():
            if package.status in ['0','1','2','11','12','20','21']:
                res.append(package)
        return res

    def count_installed(self):
        res = 0
        for package in self.packages.values():
            if package.status in ['0','1','2','11','12','20','21']:
                res += 1
        return res

    def get_packages(self):
        return self.packages

    def count_packages(self):
        return len(self.packages)
