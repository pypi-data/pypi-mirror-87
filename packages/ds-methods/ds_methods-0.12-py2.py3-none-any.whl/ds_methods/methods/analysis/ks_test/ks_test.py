from pandas import DataFrame
from scipy.stats import ks_2samp

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class KSTest(BaseMethod):
    """
    This method only works for two time series
    """
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        columns = self.options['columns']
        lhs_sample = input_data[columns[0]]
        rhs_sample = input_data[columns[1]]

        ks_test = ks_2samp(lhs_sample, rhs_sample)
        data = DataFrame(
            [ks_test],
            columns=['statistic', 'p_value'],
        )

        return MethodOutput(
            data=data,
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
