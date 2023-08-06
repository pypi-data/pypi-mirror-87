from soil.data_structures.data_structure import DataStructure
from soil.connectors.elastic_search import create_db_object


class EsDataStructure(DataStructure):
    @staticmethod
    def unserialize(_nothing, metadata, db_object):
        result = db_object.query({})
        data = next(result[0])
        MyDS = EsDataStructure(data, metadata, db_object)
        return MyDS

    def serialize(self):
        es_db_object = create_db_object(index='my-es-index')
        es_db_object.insert(self.data, id='first_id')
        return es_db_object

    def get_data(self, **args):
        return self.data
