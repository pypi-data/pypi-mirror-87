from soil import modulify, logger
# from soil.data_structures.simple_datastructure import SimpleDataStructure
from soil.data_structures.es_datastructure import EsDataStructure


@modulify(output_types=lambda *inputs, **args: [EsDataStructure])
def simple_mean(patients, aggregation_column=None):
    logger.info('This is a log from simple_mean')
    logger.debug('This is another log from simple_mean')
    if aggregation_column is None:
        raise TypeError('Expected aggregation_column parameter')
    total_sum = 0
    count = 0
    for patient in patients:
        if hasattr(patient, aggregation_column):
            val = patient[aggregation_column]
            total_sum += val
            count += 1
    return [EsDataStructure({'mean': round(total_sum / count)}, metadata={'awww': 'yeah'})]
