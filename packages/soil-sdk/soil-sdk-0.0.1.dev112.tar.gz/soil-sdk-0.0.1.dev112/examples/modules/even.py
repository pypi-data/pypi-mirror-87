from soil import modulify
from soil.data_structures.predefined.list import List


@modulify(output_types=lambda *inputs, **args: [List])
def even(input):
    return [List([i for i in input.data if i % 2 == 0], {})]
