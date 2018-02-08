#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module does
    Date created: 4/20/2016
    Date last modified: 4/25/2016
    Python Version: 2.7.10
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from models import app, db

__author__ = "pengwk"
__copyright__ = "Copyright 2016, pengwk"
__credits__ = [""]
__license__ = "Private"
__version__ = "0.1"
__maintainer__ = "pengwk"
__email__ = "pengwk2@gmail.com"
__status__ = "BraveHeart"

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# python manage.py db init
# migrate
# upgrade
if __name__ == '__main__':
    manager.run()
