'''
Soil package.
'''
from soil.modulify import modulify
from soil.data import data
from soil.alias import alias
from soil import finder
from soil.logger import logger
import soil.connectors as connectors

finder.install()

__all__ = [
    'modulify',
    'data_structures',
    'modules',
    'data',
    'alias',
    'logger',
    'connectors'
]
