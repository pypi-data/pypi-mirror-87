# coding: utf-8
import os
import sys
import hashlib
import subprocess
import tarfile
import shutil
import bz2
import filecmp

from ubik.core import conf
from ubik.logger import logger
from ubik.logger import stream_logger
from ubik.exceptions import CoreException

import ubik.package

def cached(package):
    if not isinstance(package, ubik.package.Package):
        raise CoreException('Need to be a Package object')

    if not os.path.exists(os.path.join(conf.get('settings', 'cache'), package.name + ".tar")):
        return False

    return True

def checkmd5(package):
    if not isinstance(package, ubik.package.Package):
        raise CoreException('Need to be a Package object')

    package_path = os.path.join(conf.get('settings', 'cache'), package.name + ".tar")

    fh = open(package_path, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)

    if package.md5 != m.hexdigest():
        return False
    return True

def confirm(prompt=None, resp=False):
    try:
        if prompt is None:
            prompt = 'Do you want to continue'

        if resp:
            prompt = '%s [%s|%s]? ' % (prompt, 'n', 'Y')
        else:
            prompt = '%s [%s|%s]? ' % (prompt, 'y', 'N')

        while True:
            ans = raw_input(prompt)
            if not ans:
                return resp
            if ans == 'y' or ans == 'Y':
                return True
            if ans == 'n' or ans == 'N':
                return False
            else:
                return False
    except KeyboardInterrupt:
        stream_logger.info('\nAbort.')
        sys.exit(1)

def clean():
    files = os.listdir(conf.get('settings', 'cache'))
    for f in files:
        logger.debug(f)
        if not '.tar' in f and os.path.isdir(f):
            shutil.rmtree(f)

def unarchiver(package):
    src = os.path.join(conf.get('settings', 'cache'), package.name + ".tar")
    dst = conf.get('settings', 'cache')

    # Open tarfile
    tar = tarfile.open(src)
    if tarfile.is_tarfile(src):
        tar.extractall(dst)
    else:
        raise Exception('Archive invalid (not a tarfile)')

def unpacker(package):
    archive = tarfile.open(os.path.join(conf.get('settings', 'cache'), package.name, 'files.bz2'), 'r:bz2', ignore_zeros=True)
    root_content = os.path.join(conf.get('settings', 'cache'), package.name, 'content')
    if os.path.exists(root_content):
        shutil.rmtree(root_content)
    os.makedirs(root_content)
    archive.extractall(root_content)

    for (path, dirs, files) in os.walk(root_content):
        for _dir in dirs:
            src = os.path.join(path, _dir)
            dst = '%s' % src.replace(root_content, conf.get('settings', 'packages'))
            if os.path.islink(src):
                linkto = os.readlink(src)
                os.remove(dst)
                os.symlink(linkto, dst)
            elif not os.path.exists(dst):
                os.makedirs(dst)

        for _file in files:
            src = os.path.join(path, _file)
            dst = '%s' % src.replace(root_content, conf.get('settings', 'packages'))
            # If safe_conf
            if conf.get('packages', 'safe_conf') == 'True':
                # Is etc
                if path.replace(root_content, '')[1:].split('/')[0] == 'etc':
                    # Is file in etc
                    if os.path.isfile(os.path.join(path, _file)):
                        # If file already exist
                        if os.path.exists(dst):
                            if filecmp.cmp(src, dst):
                                logger.info('CONFIG: config file not modified')
                                continue
                            logger.info('CONFIG: config file conflict: %s' % os.path.join(path, _file))
                            dst += '.new'
            logger.debug(" :: %s - %s" % (src, dst))
            if os.path.islink(src):
                linkto = os.readlink(src)

                if os.path.lexists(dst):
                    os.remove(dst)
                os.symlink(linkto, dst)

            else:
                shutil.copy2(src, dst)

    shutil.rmtree(root_content)
    archive.close()
