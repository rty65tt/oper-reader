#/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, site
import django.core.handlers.wsgi

import locale
locale.setlocale(locale.LC_TIME,'ru_RU.UTF-8')

sys.path.insert(0, '/var/www/sites')

site.addsitedir('/var/www/djenv/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'oper.settings'
os.environ['PYTHON_EGG_CACHE'] = '/var/www/sites/oper/.python-egg'

application = django.core.handlers.wsgi.WSGIHandler()


