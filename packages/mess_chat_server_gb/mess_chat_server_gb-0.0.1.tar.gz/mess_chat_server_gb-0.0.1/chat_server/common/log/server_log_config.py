"""
The chat server logs configuration
"""

import sys
import os
import logging
from logging import handlers

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)
from common.config import system


PATH = os.path.join(BASEDIR, system.LOG_DIR, 'server.log')

# A log message format
FORMATTER = logging.Formatter('%(asctime)-25s %(levelname)-15s %(module)-20s %(funcName)-20s %(message)s')

CONSOLE_LOG_HANDLER = logging.StreamHandler(sys.stderr)
CONSOLE_LOG_HANDLER.setFormatter(FORMATTER)
CONSOLE_LOG_HANDLER.setLevel(logging.WARNING)

FILE_LOG_HANDLER = handlers.TimedRotatingFileHandler(
    PATH,
    encoding=system.ENCODING,
    interval=system.LOG_INTERVAL,
    when='D'
)
FILE_LOG_HANDLER.setFormatter(FORMATTER)


LOGGER = logging.getLogger('server')
LOGGER.addHandler(CONSOLE_LOG_HANDLER)
LOGGER.addHandler(FILE_LOG_HANDLER)
LOGGER.setLevel(system.LOG_LEVEL)

if __name__ == '__main__':

    LOGGER.critical('A critical error message')
    LOGGER.error('A error message')
    LOGGER.warning('A warning message')
    LOGGER.info('A info message')
    LOGGER.debug('A debug message')
