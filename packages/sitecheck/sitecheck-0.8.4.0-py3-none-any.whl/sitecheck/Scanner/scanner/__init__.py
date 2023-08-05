"""
    Geo-Instruments
    Sitecheck Scanner
"""
# __name__ = "scanner"
# __author__ = "Dan Edens"
# __url__= "https://github.com/DanEdens/Sitecheck_Scrapper"
# __status__  = "production"

import logging
import os
import paho.mqtt.client as mqtt

logger = logging.getLogger('log')
projectstore = os.environ['ROOT_DIR'] + '/projects.ini'
hostname = os.environ.get('SCANNER_IP', 'localhost')
port = int(os.environ.get('SCANNER_port', 1884))
client = mqtt.Client("qv", clean_session=True)
client.connect(hostname, port)
