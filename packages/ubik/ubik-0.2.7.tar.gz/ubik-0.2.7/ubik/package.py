# coding: utf-8
import os
import sys
import shutil

from ubik.core import conf

from ubik.downloader import get_package

from ubik.logger import logger
from ubik.logger import stream_logger

from ubik.tools import unarchiver
from ubik.tools import unpacker

from ubik.exceptions import *

class Package(object):
    def __init__(self, name):
        self.name = name
        self.description = ''
        self.version = ''
        self.release = ''
        self.status = ''
        self.requires = []
        self.md5 = ''
        self.arch = ''
        self.dist = ''
        self.vers = ''
        self.repo_version = ''
        self.repo_release = ''

    def fill(self, **kwargs):
        for key in kwargs:
            if key == 'name':
                self.name = kwargs[key]
            elif key == 'description':
                self.description = kwargs[key]
            elif key == 'version':
                self.version = kwargs[key]
            elif key == 'release':
                self.release = kwargs[key]
            elif key == 'status':
                self.status = kwargs[key]
            elif key == 'requires':
                self.requires = kwargs[key]
            elif key == 'md5':
                self.md5 = kwargs[key]
            elif key == 'arch':
                self.arch = kwargs[key]
            elif key == 'dist':
                self.dist = kwargs[key]
            elif key == 'vers':
                self.vers = kwargs[key]
            elif key == 'repo_version':
                self.repo_version = kwargs[key]
            elif key == 'repo_release':
                self.repo_release = kwargs[key]

    def unarchive(self):
        unarchiver(self)

    def import_control(self):
        initial_dir = os.getcwd()
        #os.chdir(conf.get('settings', 'cache'))
        sys.path.append(os.path.join(conf.get('settings', 'cache'), self.name))

        # Clean control module if already loaded
        if 'control' in sys.modules:
            del sys.modules['control']

        control_module =  __import__('control')
        sys.path.remove(os.path.join(conf.get('settings', 'cache'), self.name))
        self.control = control_module.Package()
        os.chdir(initial_dir)

    def install(self, ignore_errors=False):
        # Think about ignore_errors
        stream_logger.info('    - %s' % self.name)
        stream_logger.info('      | Unarchive')
        self.unarchive()
        self.import_control()
        # Pre-install
        stream_logger.info('      | Pre Install')
        self.control.pre_install()
        stream_logger.info('      | Unpack')
        unpacker(self)
        # Post-install
        stream_logger.info('      | Post Install')
        self.control.post_install()
        stream_logger.info('      | Clean')
        shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))

    def upgrade(self, ignore_errors=False):
        # Think about ignore_errors
        stream_logger.info('    - %s' % self.name)
        stream_logger.info('      | Unarchive')
        self.unarchive()
        self.import_control()
        # Pre-upgrade
        stream_logger.info('      | Pre Upgrade')
        self.control.pre_upgrade()
        stream_logger.info('      | Unpack')
        unpacker(self)
        # Post-upgrade
        stream_logger.info('      | Post Upgrade')
        self.control.post_upgrade()
        stream_logger.info('      | Clean')
        shutil.rmtree('%s/%s' % (conf.get('settings', 'cache'), self.name))

    def remove(self, ignore_errors=False):
        # Think about ignore_errors
        stream_logger.info('   - %s' % self.name)

        # If archive not already extract
        if not os.path.exists('%s/%s' % (
                    conf.get('settings', 'cache'),
                    self.name)):
            self.unarchive()

        self.import_control()
        # Pre Remove
        stream_logger.info('     | Pre Remove')
        self.control.pre_remove()

        # Remove
        stream_logger.info('     | Remove')
        files_list = open(os.path.join(
                        conf.get('settings', 'cache'),
                        self.name,
                        'files.lst')).readlines()
        for _file in files_list:
            try:
                os.remove(os.path.join(conf.get('settings', 'packages'), _file.replace('\n', '')))
            except:
                pass
        # Post Remove
        stream_logger.info('     | Post Remove')
        self.control.post_remove()

        stream_logger.info('     | Clean')
        shutil.rmtree(os.path.join(conf.get('settings', 'cache'), self.name))
