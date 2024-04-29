"""
Constants for site checking.
"""
from enum import Enum

from admin_utils.test_params import PROJECT_ROOT

HEADERS_ATTEMPTS: list[list] = [
    [],
    ['user-agent'],
    ['user-agent', 'accept', 'accept-encoding', 'accept-language'],
    ['user-agent', 'accept', 'accept-encoding', 'accept-language', 'cookie']
]


class CheckStatuses(str, Enum):
    """
    Short summary of site check.
    """
    STATIC = 'STATIC'
    DYNAMIC = 'DYNAMIC'
    HYBRID = 'HYBRID'
    ERROR = 'ERROR'


VALIDATOR_PATH = PROJECT_ROOT / 'config' / 'website_validation'
ASSETS_PATH = VALIDATOR_PATH / 'assets'
CONFIG_PATH = ASSETS_PATH / 'validation_config.json'
BUTTONS_PATH = ASSETS_PATH / 'buttons_names.txt'

DIST_PATH = VALIDATOR_PATH / 'dist'
CSV_REPORT_PATH = DIST_PATH / 'validation_results.csv'
JSON_REPORT_PATH = DIST_PATH / 'validation_results.json'
JSON_WHITELIST_PATH = DIST_PATH / 'whitelist.json'
JSON_BLACKLIST_PATH = DIST_PATH / 'blacklist.json'
