'''
This module defines the @modulify decorator.
'''
import random
from typing import List, Dict, Any, Callable, Optional, cast
from soil.data_structure import DataStructure
from soil.pipeline import Pipeline


def _generate_data_structure_ids(fn_name: str, quantity: int) -> List[str]:
    rnd = random.randint(1000, 9999)  # nosec
    return [fn_name.replace('.', '/') + '-' + str(rnd) + '-' + str(i) for i in range(quantity)]


def _generate_transformation(
        input_ids: List[str],
        output_ids: List[str],
        fn_name: str,
        args: Dict[str, Any]
) -> Dict[str, Any]:
    tid = fn_name + '-' + str(random.randint(1000, 9999))  # nosec
    return {
        'id': tid,
        'module': fn_name,
        'inputs': input_ids,
        'outputs': output_ids,
        'args': args
    }


def modulify(
        _func: Optional[Callable[..., List[DataStructure]]] = None,
        *,
        output_types: Optional[Callable] = None,
        num_outputs: int = 1,  # pylint: disable=unused-argument
        _from_db: bool = False
) -> Callable:
    '''Decorates a function to mark it as a soil module.'''
    def decorator(fn: Callable[..., List[DataStructure]]) -> Callable:
        fnn = fn if _func is None else _func
        mod_name = fnn.__module__ + '.' + fnn.__name__
        if not _from_db and output_types is None:
            raise ValueError('@modulify: ' + mod_name + ' missing output_types')

        def decorated(*inputs: DataStructure, **kwargs: Any) -> List[DataStructure]:
            if not _from_db and output_types is not None:
                # WARNING this could fail if output_types() checks the type of *inputs
                num_outputs = len(output_types(*inputs, **kwargs))
            new_pipeline = Pipeline.merge_pipelines(*[input.pipeline for input in inputs if input.pipeline is not None])
            output_ids = _generate_data_structure_ids(mod_name, num_outputs)
            input_ids = [d.id if d.id is not None else d.sym_id for d in inputs]
            for i in input_ids:
                assert isinstance(i, str)
            transformation = _generate_transformation(
                input_ids=cast(List[str], input_ids),
                output_ids=output_ids,
                fn_name=mod_name,
                args=kwargs
            )
            new_pipeline = new_pipeline.add_transformation(transformation)
            outputs = [
                DataStructure(sym_id=sym_id, pipeline=new_pipeline)
                for sym_id in output_ids
            ]
            return outputs
        return decorated
    if _func is None:
        return decorator
    return decorator(_func)
