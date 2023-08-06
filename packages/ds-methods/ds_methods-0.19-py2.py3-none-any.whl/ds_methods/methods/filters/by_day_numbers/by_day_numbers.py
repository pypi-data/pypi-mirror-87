from pandas import DataFrame

from datetime import timedelta

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class FilterByDayNumbers(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        first_date = input_data.iloc[0]['date']
        filter_dates = [
            (first_date + timedelta(days=day - 1)).date()
            for day in self.options['days']
        ]

        return MethodOutput(
            data=input_data[input_data['date'].dt.date.isin(filter_dates)],
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'date') and\
               check_datetime(input_data['date']) and\
               max(self.options['days']) <= len(input_data.index)
