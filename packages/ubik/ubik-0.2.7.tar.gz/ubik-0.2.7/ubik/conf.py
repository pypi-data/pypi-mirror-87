# coding: utf-8
import os
import sys
import platform
import re
import isit

if isit.py3:
  from configparser import SafeConfigParser
else:
  from ConfigParser import SafeConfigParser

from ubik.exceptions import ConfigException

def get_conf(conf_path):
    """
    Read the configuration file and return it
    """
    conf_path = conf_path
    parser = SafeConfigParser()
    parser.read(conf_path)
    parser.add_section('paths')

    # Default
    parser.set('packages', 'safe_conf', 'True')

    if not parser.has_section('settings'):
        raise ConfigException('Missing settings section in configuration file')
    if not parser.has_option('settings', 'var_path'):
        raise ConfigException('Missing var_path option in settings section in configuration file')

    # Create paths
    parser.set('paths', 'local_db', os.path.join(parser.get('settings', 'var_path'), 'packages.db'))
    parser.set('paths', 'lock', os.path.join(parser.get('settings', 'var_path'), 'db.lock'))
    parser.set('paths', 'infos', os.path.join(parser.get('settings', 'var_path'), 'infos'))
    parser.set('paths', 'web_data', os.path.join(parser.get('settings', 'var_path'), 'ubik-web.dat'))

    # Detect system info
    if not parser.has_section('system'):
        parser.add_section('system')

    if not parser.has_option('system', 'arch'):
        if isit.bit32:
            parser.set('system', 'arch', 'i386')
        elif isit.bit64:
            parser.set('system', 'arch', 'x86_64')
    else:
        parser.set('system', 'arch', parser.get('system', 'arch').lower())

    if not parser.has_option('system', 'dist'):
        dist = 'unknown'
        vers = 'unknown'

        if isit.osx:
            dist = 'osx'
            vers = isit.osx_version
        elif isit.linux:
            if isit.debian:
                dist = "debian"
                if isit.debian_version:
                    vers = isit.debian_version
            elif isit.ubuntu:
                dist = "ubuntu"
                if isit.ubuntu_version:
                    vers = isit.ubuntu_version.replace('.', '')
            elif isit.centos:
                dist = "centos"
                if isit.centos_version:
                    vers = isit.centos_version
            elif isit.redhat:
                dist = "redhat"
                if isit.redhat_version:
                    vers = isit.redhat_version
            elif isit.archlinux:
                dist = "archlinux"
                if isit.archlinux_version:
                    vers = isit.archlinux_version

        parser.set('system', 'dist', dist)
        parser.set('system', 'vers', vers)
    else:
        parser.set('system', 'dist', parser.get('system', 'dist').lower())

    if parser.has_option('system', 'vers'):
        parser.set('system', 'vers', parser.get('system', 'vers').lower())

    return parser
