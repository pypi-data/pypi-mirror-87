"""
Common system configuration variables
"""

import json
import logging
import os
import sys
from json import JSONDecodeError

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

with open(file=f'{BASEDIR}/common/config/config.json', encoding='utf-8', mode='r') as c_file:
    try:
        config = json.load(c_file)
    except (JSONDecodeError, FileNotFoundError):
        config = {
            "port": 7777,
            "address": '0.0.0.0'
        }

# ======= Network configuration =======

# An IP port
IP_PORT = config.get("port", 7777)
# Server alowed IP
IP_SRV_ALLOWED = config.get("address", '0.0.0.0')
# An IP address of server
IP_ADDR_SRV = '127.0.0.1'
# The number of maximum connections to a server
MAX_CONNECTIONS = 5
# The Maximum message length (bytes)
MAX_PACKAGE_LENGTH = 2048
# Encoding
ENCODING = 'UTF-8'
# Soket timeout
TIMEOUT = 0.1


# ======= Common configuration =======

# An file log level
LOG_LEVEL = logging.DEBUG
# A log rotation interval (days)
LOG_INTERVAL = 1
# A name of dir to store logs
LOG_DIR = 'logs'
