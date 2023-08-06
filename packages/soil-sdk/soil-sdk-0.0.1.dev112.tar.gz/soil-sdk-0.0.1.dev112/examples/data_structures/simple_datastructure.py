import json
from soil.data_structures.data_structure import DataStructure


class SimpleDataStructure(DataStructure):
    @staticmethod
    def unserialize(json_data, metadata):
        MyDS = SimpleDataStructure(json.loads(next(json_data)), metadata)
        return MyDS

    def serialize(self):
        return json.dumps(self.data)

    def get_data(self, **args):
        return self.data
