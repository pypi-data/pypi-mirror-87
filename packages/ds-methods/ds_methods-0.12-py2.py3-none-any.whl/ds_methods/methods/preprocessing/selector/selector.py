from pandas import DataFrame

from ds_methods.common.validators import check_keys
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class Selector(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        include = self.options.get('include')
        exclude = self.options.get('exclude')
        if include:
            input_data = input_data[include]
        if exclude:
            input_data.drop(exclude, axis=1, inplace=True)

        return MethodOutput(
            data=input_data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, self.options.get('include', []) + self.options.get('exclude', []))
