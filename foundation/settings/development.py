# -*- coding: utf-8 -*-

#
# Copyright © 2013 by its contributors. See AUTHORS for details.
#
"Development settings."

# Import the production settings, which will be used as the base
# configuration:
from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#=-------------=#
# debug_toolbar #
#=-------------=#

INSTALLED_APPS += (
    'debug_toolbar',
)

# Add the applications necessary for development commands:
for app in (
        # django_extensions is a dependency of django_patterns, and provides
        # the ever-useful runserver_plus command for launching a Werkzeug
        # development server with integrated debugger.
        'django_extensions',

        # Provides shell_plusplus, a modification of shell_plus provided by
        # django_extensions, which launches an IPython interactive development
        # shell.
        'django_patterns'):
    if app not in INSTALLED_APPS:
        INSTALLED_APPS += (app,)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = dict()
DEBUG_TOOLBAR_CONFIG['INTERCEPT_REDIRECTS'] = False

#
# End of File
#
