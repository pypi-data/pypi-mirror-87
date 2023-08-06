# coding: utf-8
import json

import ubik.core as api

from ubik.web import lock
from ubik.web import logger
from ubik.web import sync_state

from ubik.installer import Installer
from ubik.reinstaller import Reinstaller
from ubik.remover import Remover
from ubik.upgrader import Upgrader

def log(ws, message):
    ws.send(json.dumps({'action': 'logs', 'output': message}))
    logger.add(message)

def sync(ws):
    try:
        log(ws, 'Sync database')
        api.db.sync()
        sync_state['success'] = True
        sync_state['output'] = 'Sync ok'
        sync_state['last'] = json.load(open(api.conf.get('paths', 'infos')))['last_update']
        return sync_state
    except Exception as err:
        sync_state['success'] = False
        sync_state['output'] = str(err)
        sync_state['last'] = json.load(open(api.conf.get('paths', 'infos')))['last_update']
        return sync_state

def install_package(ws, package):
    p_name = package
    if p_name in lock:
        log(ws, '<strong>Error</strong>: Someone already work with %s package' % package)
        return
    lock.append(p_name)
    try:
        log(ws, 'Sync database')
        api.db.sync()
        installer = Installer()
        package = api.db.get(package)[0]
        log(ws, 'Resolve dependencies')
        installer.resolve(package)
        installer.feed(installer.resolved)
        installed_packages = "<ul>"
        for p in installer.packages:
            installed_packages += "<li>%s</li>" % p.name
        installed_packages = installed_packages + "</ul>"
        log(ws, 'Following dependencies will be installed: %s' % installed_packages)
        log(ws, 'Download package(s)')
        installer.download()
        log(ws, 'Install package(s)')
        installer.install()
        log(ws, 'Done')
    except Exception as err:
        log(ws, '<strong>Error</strong>: %s' % err)
    lock.remove(p_name)

def reinstall_package(ws, package):
    p_name = package
    if package in lock:
        
        log(ws, '<strong>Error</strong>: Someone already work with %s package' % package)
        return
    lock.append(p_name)
    try:
        log(ws, 'Sync database')
        api.db.sync()
        reinstaller = Reinstaller()
        package = api.db.get(package)[0]
        print(package)
        log(ws, 'Resolve dependencies')
        reinstaller.resolve(package)
        reinstaller.feed(reinstaller.resolved)
        reinstalled_packages = "<ul>"
        for p in reinstaller.packages:
            reinstalled_packages += "<li>%s</li>" % p.name
        reinstalled_packages = reinstalled_packages + "</ul>"
        log(ws, 'Following dependencies will be installed: %s' % reinstalled_packages)
        log(ws, 'Download package')
        reinstaller.download()
        log(ws, 'Reinstall package')
        reinstaller.reinstall()
    except Exception as err:
        log(ws, '<strong>Error</strong>: %s' % err)
    lock.remove(p_name)

def upgrade_package(ws, package):
    p_name = package
    if p_name in lock:
        log(ws, '<strong>Error</strong>: Someone already work with %s package' % package)
        return
    lock.append(p_name)
    try:
        log(ws, 'Sync database')
        api.db.sync()
        upgrader = Upgrader()
        package = api.db.get(package)[0]
        upgrader.feed(package)
        log(ws, 'Download package')
        upgrader.download()
        log(ws, 'Upgrade package')
        upgrader.upgrade()
    except Exception as err:
        log(ws, '<strong>Error</strong>: %s' % err)
    lock.remove(p_name)

def remove_package(ws, package):
    p_name = package
    if p_name in lock:
        log(ws, '<strong>Error</strong>: Someone already work with %s package' % package)
        return
    lock.append(p_name)
    try:
        remover = Remover()
        remover.feed(package)
        log(ws, 'Remove %s' % package)
        remover.remove()
    except Exception as err:
        log(ws, '<strong>Error</strong>: %s' % err)
    lock.remove(p_name)
