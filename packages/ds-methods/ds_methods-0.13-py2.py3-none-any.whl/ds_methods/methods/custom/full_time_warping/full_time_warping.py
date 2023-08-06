from pandas import DataFrame

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput
from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.analysis import TimeWarping, TimeWarpingType
from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class FullTimeWarping(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)
        pair_column_prefix = self.options_schema['pair_column_prefix']

        data = input_data.copy()
        for column in numeric_part.columns:
            if pair_column_prefix in column:
                continue
            pair_column = f'{column}_{pair_column_prefix}'
            if pair_column not in numeric_part.columns:
                continue

            data = TimeWarping({
                'columns': [column, pair_column],
                'type': TimeWarpingType.DISTANCE,
            }).make(data)['data']
            data = data.rename({'tw_distance': f'{column}_tw_distance'})

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'date') and check_datetime(input_data['date'])
