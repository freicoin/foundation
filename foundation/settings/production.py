# -*- coding: utf-8 -*-

#
# Copyright © 2013 by its contributors. See AUTHORS for details.
#
"Production settings."

from .common import *

# Session and CSRF keys for the production site are not kept under version
# control, but rather provided by the production environment configuration.
SECRET_KEY = os.environ['SECRET_KEY']

#
# End of File
#
