'''
This package contains calls for soil alias data structures
'''
from soil.api import set_alias
from soil.data_structure import DataStructure


def alias(name: str, data_ref: DataStructure) -> None:
    ''' Set an alias to a data reference'''
    # Force to get an id if there is none yet.
    if data_ref.id is None:
        data_ref.get_data()
    assert isinstance(data_ref.id, str)
    set_alias(name, data_ref.id)
