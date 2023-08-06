import numpy as np
from pandas import DataFrame
from scipy.stats import zscore

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema, OutliersHows, OutliersMethods


class FilterOutliers(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        if self.options['method'] == OutliersMethods.Remove:
            data = self.remove_outliers(
                input_data,
                self.options['include'],
                self.options['exclude'],
                self.options['threshold'],
                self.options['how'],
            )
        else:
            data = self.get_outliers(
                input_data,
                self.options['include'],
                self.options['exclude'],
                self.options['threshold'],
                self.options['how'],
            )

        return MethodOutput(
            data=data,
            error=None,
        )

    @staticmethod
    def remove_outliers(
            data: DataFrame,
            include: list,
            exclude: list,
            threshold: float,
            how: str,
    ) -> DataFrame:
        """
        An outlier is a value that is more than 3 standard deviations from the mean
        """
        columns = list(set(include or DataFrameUtils.decompose(data)[0].columns.tolist()) - set(exclude or []))
        considered_part = data[columns]

        abs_z_scores = np.abs(zscore(considered_part))

        if how == OutliersHows.All:
            return data[(abs_z_scores < threshold).all(axis=1)]
        if how == OutliersHows.Any:
            return data[(abs_z_scores < threshold).any(axis=1)]

    @staticmethod
    def get_outliers(
            data: DataFrame,
            include: list,
            exclude: list,
            threshold: float,
            how: str,
    ) -> DataFrame:
        """
        An outlier is a value that is more than 3 standard deviations from the mean
        """
        columns = list(set(include or DataFrameUtils.decompose(data)[0].columns.tolist()) - set(exclude or []))
        considered_part = data[columns]

        abs_z_scores = np.abs(zscore(considered_part))

        if how == OutliersHows.All:
            return data[(abs_z_scores >= threshold).all(axis=1)]
        if how == OutliersHows.Any:
            return data[(abs_z_scores >= threshold).any(axis=1)]

    def validate_input_(self, input_data: DataFrame) -> bool:
        return (not self.options['include']) or check_keys(input_data, self.options['include'])
