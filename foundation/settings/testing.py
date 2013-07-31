# -*- coding: utf-8 -*-

#
# Copyright © 2013 by its contributors. See AUTHORS for details.
#
"""
Settings file for use while running unit tests during development and on the
staging server. This settings file attempts to match as closely as possible
the production settings, while providing a few configuration tweaks that are
necessary to setup a sandboxed settings environment.
"""

# Import the production settings, which will be used as the base
# configuration:
from .common import *

# Run syncdb and migrate on first run if an in-memory database is used.
MIDDLEWARE_CLASSES = (
        'django_patterns.middleware.SyncDBOnStartupMiddleware',
    ) + MIDDLEWARE_CLASSES

# The django_nose test runner uses nose under the hood (obviously) and is
# better than the default Django test runner in that it can discover and run
# tests in source files spread throughout the project (this allows tests to be
# written near the code that being tested), generates better reports, and has
# a better framework for extending its functionality through plug-ins.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Add the applications necessary for unit test discovery:
for app in (
        # Django-extensions is a dependency of Django-patterns.
        'django_extensions',

        # Provides setup and utilities for assisting test discovery.
        'django_patterns',

        # Replaces the default Django test runner with nose's, which is much
        # more capable at auto-discovery of tests and provides a better
        # framework for report generation and plug-in functionality.
        'django_nose'):
    if app not in INSTALLED_APPS:
        INSTALLED_APPS += (app,)

#
# End of File
#
