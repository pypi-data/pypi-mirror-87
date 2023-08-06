---
id: version-0.0.4-data-structures
title: Data Structures
sidebar_label: Data Structures
original_id: data-structures
---

Data Structures contain and pass the information between modules in a SOIL pipeline. They are defined in the `data_structures` package under the top level. A data structure is defined in a class that inherits from `soil.data_structures.data_structure.DataStructure` or from a class that inherits from it.

It contains two attributes **data** and **metadata**. The schemas of each are different for each data structure.

Additionally a data structure must implement three methods:
* **serialize**: To transform the data to a string to be stored in disk o a DB.
* **unserialize**: A static method to transform serialized data to actual data.
* **get_data**: Returns a jsonable object to send the data to the client.

The signature of the init method is: `__init__(data, metadata=None)`

Optionally you can implement the **export(format='csv')** method that when called will generate a zip file with the data contained in the data structure.

The following example serializes and unserializes json.

```py
import json
from soil.data_structures.data_structure import DataStructure

class Statistics(DataStructure):
    @staticmethod
    def unserialize(str_lines, metadata, db_object=None):
        return Statistics(json.loads(next(str_lines)), metadata)

    def serialize(self):
        return json.dumps(self.data)

    def get_data(self, **args):
        return self.data
```

## Insert to a DB (not implemented)
Right now data can only be stored in disk and Elastic Search. To store to disk you only need to return a json or a generator of json objects in serialize.
To store something to a db you need to obtain a db_object first. You can create a db_object from `soil.connectors.elastic_search.create_db_object()`

```py
from soil.data_structures.data_structure import DataStructure
from soil.connectors.elastic_search import create_db_object

class MyDS(DataStructure):
    def serialize(self):
        es_db_object = create_db_object(index='my-es-index')
        for d in self.data:
            es_db_object.insert(d)
        return es_db_object
```


## Read from a data base

To read from a DB you can use the db_object element passed in the unserialize method. To query the data base use `db_object.query(query)`

### Optimization: Lazy DB queries.

TODO

## Streams

TODO
