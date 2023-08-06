import soil
import logging
from soil.modules.even import even

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

data_ref = soil.data([i for i in range(50)])

soil.alias('my_data2', data_ref)

data_ref2 = soil.data('my_data2')
even_numbers, = even(data_ref2)
for i in even_numbers.data:
    print(i)
