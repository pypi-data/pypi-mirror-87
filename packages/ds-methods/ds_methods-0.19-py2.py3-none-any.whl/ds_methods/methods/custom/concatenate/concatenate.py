from pandas import DataFrame, concat

from ds_methods.common.decorators import catch_method_error
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class Concatenate(BaseMethod):
    options_schema = options_schema

    @catch_method_error()
    def make(self, input_data: [DataFrame]) -> MethodOutput:
        if any(data.empty for data in input_data):
            return MethodOutput(error='empty input')
        if not self.validate_input_(input_data):
            return MethodOutput(error='wrong input format')

        return self.make_(input_data)

    def make_(self, input_data: [DataFrame]) -> MethodOutput:
        prefixes = list(set(self.options_schema['prefixes']))
        axis = self.options_schema['axis']

        if axis == 1:
            for index in range(len(input_data)):
                input_data[index] = input_data[index].rename(
                    lambda name: f'{name}_{prefixes[index]}',
                    axis='columns',
                )

        data = concat(input_data, axis=axis)

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: [DataFrame]) -> bool:
        return len(set(self.options_schema['prefixes'])) == len(input_data)
