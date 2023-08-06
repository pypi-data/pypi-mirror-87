from typing import List
from functools import partial
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy

from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod
from ds_methods.methods.preprocessing import Basic


class Pipeline:
    def __init__(self, methods: List):
        self.methods = methods

    def run(self, input_data: DataFrame) -> MethodOutput:
        for method in self.methods:
            print('\n\n', method.__class__.__name__)
            if isinstance(input_data, DataFrameGroupBy):
                apply_function = partial(Pipeline.apply_function, method=method)
                input_data = Basic.reset_index(
                    input_data.apply(apply_function),
                )
            elif isinstance(input_data, DataFrame):
                output = method.make(input_data)
                if output['error']:
                    return MethodOutput(error=output['error'])

                input_data = output['data']

            print(input_data, '\n\n')
        return MethodOutput(data=input_data, error=None)

    @staticmethod
    def apply_function(input_data: DataFrame, method: BaseMethod) -> DataFrame:
        data = method.make(input_data)
        if data['error']:
            raise Exception(data['error'])

        return data['data']
