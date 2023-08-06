from pandas import DataFrame

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class FilterByDayTime(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        filters = 1
        if 'gte' in self.options:
            filters &= input_data['date'].dt.time >= self.options['gte']
            # filters.append(f"date >= '{self.options['gte']}'")
        if 'lte' in self.options:
            filters &= input_data['date'].dt.time <= self.options['lte']
            # filters.append(f"date <= '{self.options['lte']}'")

        return MethodOutput(
            data=input_data[filters],
            # data=input_data[
            #     (self.options['gte'] <= input_data['date'].dt.time) &
            #     (input_data['date'].dt.time <= self.options['lte'])
            # ],
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'date') and check_datetime(input_data['date'])
