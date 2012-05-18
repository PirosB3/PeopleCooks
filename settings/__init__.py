# -*- coding: utf-8 -*-

# Configuration
DEBUG = False
SECRET_KEY = '9r8h8239e7986h*/whefhefiwkjnkdcnjksa+)(Y£"'

# Database settings
DATABASE_NAME = 'recipes'

# Auth settings
AUTH_USERNAME = 'username'
AUTH_PASSWORD = 'password'

# Import local settings
try:
    from local_settings import *
except ImportError:
    pass
