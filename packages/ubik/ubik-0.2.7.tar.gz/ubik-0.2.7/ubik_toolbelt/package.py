# coding: utf-8
from __future__ import with_statement

import os
import sys
import shutil
import tarfile

from ubik_toolbelt.logger import stream_logger

def create(package_name):
	name = package_name

	control_py = """# coding: utf-8
import os

from ubik_toolbelt.logger import stream_logger
from ubik_toolbelt.control import Control

class Package(Control):
    \"\"\"
        Control object attributs ::
            self.cur_dir    Current directory
            self.src_dir    Source directory
            self.pkg_dir    Build directory

        Help ::
            http://ubik.socketubs.net/toolbelt/packager.html
    \"\"\"
    def __init__(self):
        Control.__init__(self)
        self.name = '%s'
        self.version = ''
        self.release = '0'
        self.requires = []
        self.arch = ''
        self.dist = ''
        self.vers = ''
        self.description = ''

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
""" % name

	stream_logger.info(' :: Create %s package structure' % name)
	os.makedirs(name)
	os.chdir(name)
	os.makedirs('build')
	os.makedirs('source')
	with open('control.py', 'w') as control:
		control.write(control_py)
	stream_logger.info(' :: Done')

def build():
    sys.path.append(os.getcwd())
    control = __import__('control', globals(), locals(), [], 0)
    sys.path.remove(os.getcwd())
    control = control.Package()
    control.build()

def package():
    sys.path.append(os.getcwd())
    control = __import__('control', globals(), locals(), [], 0)
    sys.path.remove(os.getcwd())
    control = control.Package()
    control.package()

def archive():
    sys.path.append(os.getcwd())
    control = __import__('control', globals(), locals(), [], 0)
    sys.path.remove(os.getcwd())
    control = control.Package()

    if os.path.exists(control.name):
        stream_logger.info('Package already archived')
        sys.exit(1)

    os.makedirs(control.name)

    with open(os.path.join(control.name, 'files.lst'), 'w') as list_file:
        _pwd = os.getcwd()
        os.chdir('build')
        for (p,d,f) in os.walk('.'):
            for _f in f:
                list_file.write(os.path.join(p, _f) + '\n')
        os.chdir(_pwd)

    create_tar('build', os.path.join(control.name, 'files.bz2'), change_dir=True, mode='w:bz2')
    shutil.copyfile('control.py', os.path.join(control.name, 'control.py'))
    create_tar(control.name, '%s.tar' % control.name)

def create_tar(src, dst, change_dir=False, mode='w'):

    """
    Mode  Description
        r        Opens a TAR file for reading
        r:       Opens a TAR file for reading with no compression
        w or w:  Opens a TAR file for writing with no compression
        a or a:  Opens a TAR file for appending with no compression
        r:gz     Opens a TAR file for reading with gzip compression
        w:gz     Opens a TAR file for writing with gzip compression
        r:bz2    Opens a TAR file for reading with bzip2 compression
        w:bz2    Opens a TAR file for writing with bzip2 compression
    """

    tar_file = tarfile.open(dst, mode)

    files = os.listdir(src)
    _pwd = os.getcwd()

    if change_dir:
        os.chdir(src)

    for f in files:
        if change_dir:
            tar_file.add(f)
        else:
            tar_file.add(os.path.join(src, f))

    tar_file.close()
    os.chdir(_pwd)
