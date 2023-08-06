''' Defines the configuration for Soil '''
from typing import Optional, NamedTuple
import logging
from os import getenv
import json
import requests
# TODO add windows support

# pylint: disable=invalid-name
env = getenv('PY_ENV', 'development')


def _refresh_token(auth_host: str, refresh_token: str) -> str:
    url = auth_host + '/api/jwt/refresh'
    response = requests.post(url, json={'refreshToken': refresh_token})
    if response.status_code != 200:
        raise ValueError('Invalid refresh token please run soil login again.')
    return json.loads(response.text)['token']


SOIL_URL = ''
if env != 'test':
    try:
        with open(getenv('HOME', '') + '/.soil/soil.conf') as conf_file:
            CONF = json.loads(conf_file.read())
            SOIL_URL = CONF['soil_url']
    except FileNotFoundError:
        logging.warning('~/.soil/soil.conf file not found. Please run soil configure.')
else:
    SOIL_URL = 'http://test_host.test'

TOKEN = ''  # nosec

if env != 'test':
    try:
        with open(getenv('HOME', '') + '/.soil/soil.env') as env_file:
            ENV = json.loads(env_file.read())
            TOKEN = _refresh_token(CONF['auth_url'], ENV['auth']['refreshToken'])
    except FileNotFoundError:
        logging.warning('~/.soil/soil.env file not found. Please run soil login.')
else:
    TOKEN = 'test_token'  # nosec

DEFAULT_CONFIG = {
    'host': getenv('SOIL_HOST', SOIL_URL),
    'token': getenv('SOIL_TOKEN', TOKEN)
}


class SoilConfiguration(NamedTuple):
    ''' Soil configuration class '''
    host: Optional[str]
    token: Optional[str]


GLOBAL_CONFIG = SoilConfiguration(**DEFAULT_CONFIG)


# Not used for now
# def config(token: Optional[str] = None, host: Optional[str] = None) -> SoilConfiguration:
#     ''' Set the Soil's configuration '''
#     global GLOBAL_CONFIG  # pylint: disable=global-statement
#     new_config = SoilConfiguration(token=token, host=host)
#     GLOBAL_CONFIG = SoilConfiguration(**{**GLOBAL_CONFIG._asdict(), **new_config._asdict()})
#     return GLOBAL_CONFIG
