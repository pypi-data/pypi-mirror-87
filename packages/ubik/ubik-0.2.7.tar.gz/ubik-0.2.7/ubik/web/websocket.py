# coding: utf-8
import json

from helpers import install_package
from helpers import reinstall_package
from helpers import upgrade_package
from helpers import remove_package
from helpers import sync

from ubik.web import logger
from ubik.web import sync_state

def handle_websocket(ws):
    while True:
        res = {}
        message = ws.receive()
        if message is None:
            break
        else:
             message = json.loads(message)

        if message['action'] == 'sync':
            res = sync(ws)
            res['action'] = 'sync_state'
            ws.send(json.dumps(res))
        elif message['action'] == 'sync_state':
            res['action'] = 'sync_state'
            res = dict(res.items() + sync_state.items())
            ws.send(json.dumps(res))
        elif message['action'] == 'install':
            install_package(ws, message['package'])
        elif message['action'] == 'reinstall':
            reinstall_package(ws, message['package'])
        elif message['action'] == 'remove':
            remove_package(ws, message['package'])
        elif message['action'] == 'upgrade':
            upgrade_package(ws, message['package'])
        elif message['action'] == 'get_logs':
            ws.send(json.dumps({'action': 'get_logs', 'logs': logger.get_logs()}))