from pandas import DataFrame, Grouper
import pandas as pd

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput
from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.preprocessing import Selector
from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class AverageDay(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        day_groups = input_data.groupby(Grouper(freq='1D', key='date'), as_index=False, sort=False)

        #  filter not full days
        data = day_groups.filter(
            lambda group: (group['date'].iloc[0].hour < 3) and (group['date'].iloc[-1].hour > 21)
        ).reset_index(drop=True)

        # re-sample
        data['times'] = data['date'].dt.time
        all_times = DataFrame({'times': sorted(set(data['times']))}).reset_index(drop=True)
        data = data\
            .groupby(Grouper(freq='1D', key='date'), as_index=False, sort=False)\
            .apply(lambda group: group.merge(all_times, on='times', how='right'))\
            .fillna(method='ffill')\
            .groupby(by='times', as_index=False, sort=False).aggregate({
                **{key: 'first' for key in other_part.columns},
                **{key: 'mean' for key in numeric_part.columns},
            })

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'date') and check_datetime(input_data['date'])
