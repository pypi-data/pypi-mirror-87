from pandas import DataFrame

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class FilterByDate(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        filters = 1
        if 'gte' in self.options:
            filters &= input_data['date'] >= self.options['gte'].replace(tzinfo=None)
            # filters.append(f"date >= '{options['gte']}'")
        if 'lte' in self.options:
            filters &= input_data['date'] <= self.options['lte'].replace(tzinfo=None)
            # filters.append(f"date <= '{options['lte']}'")

        return MethodOutput(
            data=input_data[filters],
            # data=eval_df_query(input_data, ' and '.join(filters)),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'date') and check_datetime(input_data['date'])
