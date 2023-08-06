from typing import List
from functools import partial
from pandas import DataFrame, Series
from statsmodels.tsa.seasonal import seasonal_decompose

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class SeasonalDecomposition(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)
        decompose_function = partial(SeasonalDecomposition.seasonal_decomposition, period=self.options['period'])
        numeric_part = numeric_part.apply(decompose_function)

        return MethodOutput(
            data=DataFrameUtils.concatenate([other_part, numeric_part]),
            error=None,
        )

    @staticmethod
    def seasonal_decomposition(input_data: Series, period: int) -> List:
        return seasonal_decompose(input_data, period=period, extrapolate_trend=False).trend

    def validate_input_(self, input_data: DataFrame) -> bool:
        return self.options['period'] <= len(input_data.index) // 2
