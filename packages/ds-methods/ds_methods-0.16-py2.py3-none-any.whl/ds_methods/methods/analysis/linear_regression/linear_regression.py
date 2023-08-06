from pandas import DataFrame
from sklearn.linear_model import LinearRegression as sklearnLinearRgression

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class LinearRegression(BaseMethod):
    """
    This method only works for two time series
    """
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        columns = self.options['columns']
        query = input_data[columns[0]].to_numpy()
        reference = input_data[columns[1]].to_numpy()

        model = sklearnLinearRgression()
        model.fit(query, reference)

        data = []

        return MethodOutput(
            data=DataFrameUtils.concatenate([input_data, data]),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        """
        check if numeric part contains selected columns
        """
        return check_keys(
            DataFrameUtils.decompose(input_data)[0],
            self.options['columns'],
        )
