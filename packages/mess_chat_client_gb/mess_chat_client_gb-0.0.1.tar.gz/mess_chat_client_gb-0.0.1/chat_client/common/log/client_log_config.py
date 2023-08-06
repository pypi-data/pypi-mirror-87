"""
The chat client logs configuration
"""

import sys
import os
import logging

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)
from common.config import system


PATH = os.path.join(BASEDIR, system.LOG_DIR, 'client.log')

# A log message format
FORMATTER = logging.Formatter('%(asctime)-25s %(levelname)-15s %(module)-20s %(funcName)-20s %(message)s')

CONSOLE_LOG_HANDLER = logging.StreamHandler(sys.stderr)
CONSOLE_LOG_HANDLER.setFormatter(FORMATTER)
CONSOLE_LOG_HANDLER.setLevel(logging.ERROR)  # The errors only

FILE_LOG_HANDLER = logging.FileHandler(PATH, encoding=system.ENCODING)
FILE_LOG_HANDLER.setFormatter(FORMATTER)


LOGGER = logging.getLogger('client')
LOGGER.addHandler(CONSOLE_LOG_HANDLER)
LOGGER.addHandler(FILE_LOG_HANDLER)
LOGGER.setLevel(system.LOG_LEVEL)

if __name__ == '__main__':

    LOGGER.critical('A critical error message')
    LOGGER.error('A error message')
    LOGGER.warning('A warning message')
    LOGGER.info('A info message')
    LOGGER.debug('A debug message')
