---
id: version-0.0.6-data-structures
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

## Insert to a data base (experimental)
Right now data can only be stored in disk and Elastic Search. To store to disk you only need to return a json or a generator of json objects in serialize.
To store something to a db you need to obtain a db_object first. You can create a db_object from `soil.connectors.elastic_search.create_db_object(index, schema=None, force_rewrite=False)`

* You must specify the index and optionally the `schema` using the mappings as specified [here](https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-create-index.html#indices-create-api-request-body).

* If `force_rewrite` is set to true the index will be deleted before creating a new one.

* If the index was already created, `schema` will be ignored unless `force_rewrite` is set to true.

* Use `db_object.insert(obj, id=None)` to add new elements to the index. If `id` already exists it will rewrite the document. If `id` is None a new id will be created.

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


## Read from a data base (experimental)

To read from a DB you can use the db_object element passed in the unserialize method (`unserialize(data, metadata, db_object)`). To query the data base use `db_object.query(query, random_sorting=False)`. The result of a query consists in two elements a results generator which can be iterated and the rest of the data associated to the query ([which can be seen here](https://www.elastic.co/guide/en/elasticsearch/reference/master/search-search.html#search-api-response-body)) except the `'hits'`.

* Scrolling is handled automatically.
* `random_sorting=True` will sort the results randomly. It is not comapatible with other sorting methods. **It can be useful to do sampling automatically**.


### Optimization: Lazy DB queries and Streams (experimental)

Sometimes it is useful to delay a query to wait if it can be combined with another more restrictive query. For example the filters on streams are a good example. Streams are the data structures that inherit from `soil.data_structures.streams.Streams`. Streams that come from a db can wait to run a query until the attribute `data` is accessed, when some part of the program needs to access the data.

You can use `db_object.update_query(new_partial_query)` to set the query that will run when the data attribute is accessed. The current query can be accessed from `db_object.partial_query`.

It is also possible to use the update_query method in combination with data structures that don't inherit from Stream, but you will have to program the logic yourself.
