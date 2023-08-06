# coding: utf-8
import os

from ubik_toolbelt.logger import stream_logger

class Control(object):
    def __init__(self):
        self.name = ''
        self.version = '0'
        self.release = '0'
        self.requires = []
        self.arch = ''
        self.dist = ''
        self.vers = ''
        self.description = ''

        self.cur_dir = os.getcwd()
        self.src_dir = os.path.join(os.getcwd(), 'source')
        self.pkg_dir = os.path.join(os.getcwd(), 'build')

    def build(self):
        stream_logger.info('Building...')

    def package(self):
        stream_logger.info('Packaging...')

    def pre_install(self):
        pass

    def post_install(self):
        pass

    def pre_upgrade(self):
        pass

    def post_upgrade(self):
        pass

    def pre_remove(self):
        pass

    def post_remove(self):
        pass
