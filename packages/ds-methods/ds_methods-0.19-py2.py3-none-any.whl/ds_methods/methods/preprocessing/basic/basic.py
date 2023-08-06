from pandas import Series, DataFrame

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import BasicMethod, options_schema


class Basic(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(
            input_data,
            include=['number', 'datetime'],
        )
        method = self.options['method']
        if method == BasicMethod.MIN:
            numeric_part = Basic.min(numeric_part)
        elif method == BasicMethod.MAX:
            numeric_part = Basic.max(numeric_part)
        elif method == BasicMethod.MEAN:
            numeric_part = Basic.mean(numeric_part)
        elif method == BasicMethod.MEDIAN:
            numeric_part = Basic.median(numeric_part)
        elif method == BasicMethod.STD:
            numeric_part = Basic.std(numeric_part)
        elif method == BasicMethod.IQR:
            numeric_part = Basic.iqr(numeric_part)

        return MethodOutput(
            data=DataFrameUtils.concatenate([
                other_part[:1],
                numeric_part.to_frame().T if isinstance(numeric_part, Series) else numeric_part,
            ]),
            error=None,
        )

    @staticmethod
    def min(input_data: DataFrame) -> Series:
        return input_data.min(numeric_only=True)

    @staticmethod
    def max(input_data: DataFrame) -> Series:
        return input_data.min(numeric_only=True)

    @staticmethod
    def mean(input_data: DataFrame) -> Series:
        return input_data.mean(numeric_only=True)

    @staticmethod
    def median(input_data: DataFrame) -> Series:
        return input_data.median(numeric_only=True)

    @staticmethod
    def std(input_data: DataFrame) -> Series:
        return input_data.std(numeric_only=True)

    @staticmethod
    def iqr(input_data: DataFrame) -> DataFrame:
        return input_data.quantile(q=.75, numeric_only=True) - input_data.quantile(q=.25, numeric_only=True)

    @staticmethod
    def reset_index(input_data: DataFrame) -> DataFrame:
        index_levels = [name for name in input_data.index.names if name]
        already_columns = [name for name in index_levels if name in input_data.columns]

        return input_data\
            .reset_index([
                name for name in index_levels
                if name not in already_columns
            ])\
            .reset_index(drop=True)
