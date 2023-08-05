"""
    Geo-Instruments
    Sitecheck Scanner
    Endpoints module for Scanner

"""
import logging
logger = logging.getLogger('server')


class parse:

    def __init__(self, userdata, message):
        self.userdata = userdata
        self.message = message
        self.payload = message.payload

    def filter_messages(self):
        if self.payload == 'test':
            logger.info('Test success')
        elif self.payload == '':
            logger.debug(f'Command recieved {self.payload}')
