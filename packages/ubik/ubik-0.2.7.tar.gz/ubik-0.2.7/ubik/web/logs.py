# coding: utf-8
import os
import pickle

import ubik.core as api

class Logger(object):
    def __init__(self):
        self.path = api.conf.get('paths', 'web_data')
        self.logs = []
        self.max_entries = 20

        if os.path.exists(self.path):
            try:
                self.logs = pickle.load(open(self.path))
            except:
                pass

    def add(self, message):
        self.logs.append(message)
        self.clean()

    def save(self):
        pickle.dump(self.logs, open(self.path, 'w'))

    def clean(self):
        self.logs = self.logs[-self.max_entries:]

    def get_logs(self):
        res = []
        for log in reversed(self.logs):
            res.insert(0, log)
        return res

logger = Logger()