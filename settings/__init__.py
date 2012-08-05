# -*- coding: utf-8 -*-

import os

# Configuration
DEBUG = False
SECRET_KEY = '9r8h8239e7986h*/whefhefiwkjnkdcnjksa+)(Y£"'
ADDRESS = ':'.join(['0.0.0.0', os.environ.get('PORT', '5000')])

# Database settings
DATABASE_NAME = 'recipes'

# Auth settings
AUTH_USERNAME = 'username'
AUTH_PASSWORD = 'password'

# Mongodb settings
MONGO_URL = os.environ.get('MONGOHQ_URL', 'mongodb://admin:password@localhost:27017/peoplecooks')
MONGO_URL_TESTING = 'mongodb://admin:password@localhost:27017/test'

# Import local settings
try:
    from local_settings import *
except ImportError:
    pass
