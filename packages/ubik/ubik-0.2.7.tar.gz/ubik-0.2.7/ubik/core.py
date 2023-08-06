#!/usr/bin/env python
# coding: utf-8
import os
import json

from ubik.conf import get_conf
from ubik.exceptions import CoreException

###################
# conf            #
###################
conf_file = os.environ.get('UBIK_CONF', '/etc/ubik.conf')
if not os.path.exists(conf_file):
	raise CoreException('Configuration file not found (%s)\nSet UBIK_CONF env variable' % conf_file)
conf = get_conf(conf_file)

###################
# Init env        #
###################
try:
	os.makedirs(conf.get('settings', 'var_path'))
	os.makedirs(conf.get('settings', 'cache'))
except:
	pass

###################
# Loggers         #
###################
from ubik.logger import logger

###################
# Database        #
###################
from ubik.database import Database
if not os.path.exists(conf.get('paths', 'local_db')):
	logger.warning('No packages.db found, is it normal ?')
	with open(conf.get('paths', 'local_db'), 'w') as f:
		f.write('[]')
db = Database(file_path=conf.get('paths', 'local_db'))
