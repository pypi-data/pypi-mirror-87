from pandas import DataFrame
from scipy.stats import zscore

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import NormalisationType, options_schema


class Normalisation(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)
        normalisation_type = self.options['type']

        if normalisation_type == NormalisationType.MIN_MAX:
            numeric_part = self.min_max(numeric_part)
        elif normalisation_type == NormalisationType.MEAN:
            numeric_part = self.mean(numeric_part)
        elif normalisation_type == NormalisationType.Z_SCORE:
            numeric_part = self.z_score(numeric_part)

        return MethodOutput(
            data=DataFrameUtils.concatenate([other_part, numeric_part]),
            error=None,
        )

    @staticmethod
    def min_max(input_data: DataFrame) -> DataFrame:
        data_min = input_data.min()

        return (input_data - data_min) / (input_data.max() - data_min)

    @staticmethod
    def mean(input_data: DataFrame) -> DataFrame:
        return (input_data - input_data.mean()) / (input_data.max() - input_data.min())

    @staticmethod
    def z_score(input_data: DataFrame) -> DataFrame:
        return input_data.apply(zscore)

    def validate_input_(self, input_data: DataFrame) -> bool:
        return True
