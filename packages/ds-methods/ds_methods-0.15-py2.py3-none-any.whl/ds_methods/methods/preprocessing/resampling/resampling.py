from pandas import DataFrame

from ds_methods.common.types import MethodOutput
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.validators import check_keys, check_datetime

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class Resampling(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        data = input_data \
            .resample(self.options['rule'], on='date').apply({
            **{key: 'first' for key in other_part.columns},
            **{key: 'mean' for key in numeric_part.columns},
        }).drop(['date'], axis=1).reset_index() \
            .fillna(method='ffill')

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, ['date']) and check_datetime(input_data['date'])
