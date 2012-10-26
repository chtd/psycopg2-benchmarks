#!/usr/bin/env python

import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('.')

from app.models import SomeModel

print SomeModel.objects.all()
