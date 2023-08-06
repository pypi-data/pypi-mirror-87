import logging
import soil # NOQA
from soil.modules.preprocessing.filters import row_filter # NOQA
from soil.modules.simple_module import simple_mean # NOQA
from soil.modules.statistics.statistics import Statistics # NOQA

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

patients = soil.data('5ece3f310af3725d0a7d76b6')
older, = row_filter.RowFilter(patients, age={'gte': 60})
women, = row_filter.RowFilter(older, sex={'eql': '1'})
# statistics, = Statistics(women, operations=[{
#             'operation_name': 'mean_age',
#             'fn': 'mean',
#             'aggregation_variable': {'name': 'age'},
#             'partition_variables': [{'name': 'sex'}]
#         }])
statistics, = simple_mean(women, aggregation_column='age')
print(statistics.data)
