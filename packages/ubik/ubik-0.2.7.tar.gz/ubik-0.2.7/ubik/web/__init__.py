#!/usr/bin/env python
# coding: utf-8
import os
import json 

from flask import Flask

from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt


import ubik.core as api

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

# BCrypt
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.setup_app(app)

# Users
from ubik.web.auth import auth_db

# auth_db.addUser('admin', 'admin')
# auth_db.addUser('socketubs', 'socketubs', active=False)

lock = []
sync_state = {  'success': None,
                'output': 'Never synced here',
                'last': json.load(open(api.conf.get('paths', 'infos')))['last_update']}

from ubik.web.logs import logger
from ubik.web.websocket import handle_websocket

# Ubik-Web app
def ubik_web(environ, start_response):  
    path = environ["PATH_INFO"]  
    if path == "/":  
        return app(environ, start_response)  
    elif path == "/websocket":  
        handle_websocket(environ["wsgi.websocket"])   
    else:  
        return app(environ, start_response)  

from ubik.web import views