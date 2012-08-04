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
MONGO_ADDRESS = 'localhost'
MONGO_PORT = 27017

# Import local settings
try:
    from local_settings import *
except ImportError:
    pass
