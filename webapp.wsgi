#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/djerty_website/")
sys.path.append("/var/www/djerty_website/webApp/")

from webApp import app as application
application.secret_key = 'hassan84226'

