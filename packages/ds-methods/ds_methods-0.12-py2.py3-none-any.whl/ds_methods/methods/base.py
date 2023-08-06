from typing import Dict
from pandas import DataFrame
from schema import Schema

from ds_methods.common.decorators import catch_method_error
from ds_methods.common.types import MethodOutput


class BaseMethod:
    options: Dict = None
    options_schema: Schema = None

    def __init__(self, options: Dict):
        if self.options_schema:
            try:
                self.options = self.options_schema.validate(options)
            except Exception as e:
                raise Exception('options are not valid', e)

    @catch_method_error()
    def make(self, input_data: DataFrame) -> MethodOutput:
        if input_data.empty:
            return MethodOutput(error='empty input')
        if not self.validate_input(input_data):
            return MethodOutput(error='wrong input format')

        return self.make_(input_data)

    def validate_input(self, input_data: DataFrame) -> bool:
        return self.validate_input_(input_data)

    @classmethod
    def make_(cls, input_data: DataFrame) -> MethodOutput:
        pass

    @classmethod
    def validate_input_(cls, input_data: DataFrame) -> bool:
        return True

    @classmethod
    def check_options(cls, options: Dict) -> bool:
        if cls.options_schema:
            try:
                cls.options_schema.validate(options)
            except Exception as e:
                print(e)
            return cls.options_schema.is_valid(options)

        return True
