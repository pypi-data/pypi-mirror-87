# -*- coding: utf-8 -*-
import os
import json

from flask.ext.login import UserMixin

import ubik.core as api

from ubik.web import login_manager
from ubik.web import bcrypt

class AuthDB(object):

    def __init__(self, database_file=None):
        self.database_file = database_file

        if self.database_file is None:
            self.db = self.newDB()
        else:
            self.retrieveDB()

    def retrieveDB(self):
        if not os.path.exists(self.database_file):
            self.db = self.newDB()
        try:
            users = json.load(open(self.database_file))
            self.db = {}
            for user in users:
                _id = self.get_id()
                new_user = User(user['username'], user['password'], _id)
                self.db[_id] = new_user
        except:
            return self.newDB()

    def newDB(self):
        return dict()

    def addUser(self, name, password, active=True):
        if name in [_user.name for _user in self.db.values()]:
            raise Exception('Username already exist')

        _id = self.get_id()
        new_user = User(name, bcrypt.generate_password_hash(password), _id, active)
        self.db[_id] = new_user

    def getUser(self, name):
        try:
            return [user for user in self.db.values() if user.name == name.lower()][0]
        except IndexError:
            raise Exception('User not exist')

    def challenge(self, name, password):
        try:
            user = self.getUser(name)
        except:
            return False
        return bcrypt.check_password_hash(user.password, password)

    def get_id(self):
        try:
            return max(self.db.keys()) + 1
        except ValueError:
            return 0

class User(UserMixin):
    def __init__(self, name, password, id, active=True):
        self.name = name.lower()
        self.password = password
        self.id = id
        self.active = active
    
    def is_active(self):
        return self.active

auth_db = AuthDB(database_file=api.conf.get('webui', 'users_file'))

@login_manager.user_loader
def load_user(id):
    return auth_db.db.get(int(id))
