'''
Configure logging
'''

import os


import logging
log = logging.getLogger(__name__)


def setup(level=None):
    '''
    Setup logging with basic defaults

    Calling this method is not required to enable logging.
    You can configure logging module in any way you prefer using its API and docs.
    '''
    template = '%(levelname)-8s %(message)s'
    logging.basicConfig(format=template)
    if level is None:
        if os.getenv('DEBUG'):
            level = logging.DEBUG
        else:
            level = logging.WARNING
    log.level = level
    log.debug('Basic defaults loaded for logger: %s', log)
