"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""


import os
from collections import namedtuple
from os.path import dirname
from pathlib import Path

from appdirs import AppDirs

import nucypher
from nucypher.exceptions import DevelopmentInstallationRequired

# Environment variables
NUCYPHER_ENVVAR_KEYRING_PASSWORD = "NUCYPHER_KEYRING_PASSWORD"
NUCYPHER_ENVVAR_WORKER_ADDRESS = "NUCYPHER_WORKER_ADDRESS"
NUCYPHER_ENVVAR_WORKER_ETH_PASSWORD = "NUCYPHER_WORKER_ETH_PASSWORD"
NUCYPHER_ENVVAR_ALICE_ETH_PASSWORD = "NUCYPHER_ALICE_ETH_PASSWORD"
NUCYPHER_ENVVAR_PROVIDER_URI = "NUCYPHER_PROVIDER_URI"
NUCYPHER_ENVVAR_WORKER_IP_ADDRESS = 'NUCYPHER_WORKER_IP_ADDRESS'


# Base Filepaths
NUCYPHER_PACKAGE = Path(nucypher.__file__).parent.resolve()
BASE_DIR = NUCYPHER_PACKAGE.parent.resolve()
DEPLOY_DIR = BASE_DIR / 'deploy'

# Test Filepaths
try:
    import tests
except ImportError:
    raise DevelopmentInstallationRequired(importable_name='tests')
else:
    # TODO: Another way to handle this situation?
    # __file__ can be None, especially with namespace packages on
    # Python 3.7 or when using apidoc and sphinx-build.
    file_path = tests.__file__
    NUCYPHER_TEST_DIR = dirname(file_path) if file_path is not None else str()

# User Application Filepaths
APP_DIR = AppDirs(nucypher.__title__, nucypher.__author__)
DEFAULT_CONFIG_ROOT = os.getenv('NUCYPHER_CONFIG_ROOT', default=APP_DIR.user_data_dir)
USER_LOG_DIR = os.getenv('NUCYPHER_USER_LOG_DIR', default=APP_DIR.user_log_dir)
DEFAULT_LOG_FILENAME = "nucypher.log"
DEFAULT_JSON_LOG_FILENAME = "nucypher.json"


# Static Seednodes
SeednodeMetadata = namedtuple('seednode', ['checksum_address', 'rest_host', 'rest_port'])
SEEDNODES = tuple()


# Sentry (Add your public key and user ID below)
NUCYPHER_SENTRY_PUBLIC_KEY = ""
NUCYPHER_SENTRY_USER_ID = ""
NUCYPHER_SENTRY_ENDPOINT = f"https://{NUCYPHER_SENTRY_PUBLIC_KEY}@sentry.io/{NUCYPHER_SENTRY_USER_ID}"


# Web
CLI_ROOT = NUCYPHER_PACKAGE / 'network' / 'templates'
TEMPLATES_DIR = CLI_ROOT / 'templates'
MAX_UPLOAD_CONTENT_LENGTH = 1024 * 50


# Dev Mode
TEMPORARY_DOMAIN = ":temporary-domain:"  # for use with `--dev` node runtimes


# Event Blocks Throttling
NUCYPHER_EVENTS_THROTTLE_MAX_BLOCKS = 'NUCYPHER_EVENTS_THROTTLE_MAX_BLOCKS'
