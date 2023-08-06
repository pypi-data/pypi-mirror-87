from pandas import DataFrame
from dtw import dtw, warp, DTW

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import TimeWarpingType, options_schema


class TimeWarping(BaseMethod):
    """
    This method only works for two time series
    """
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        columns = self.options['columns']
        query = input_data[columns[0]].to_numpy()
        reference = input_data[columns[1]].to_numpy()

        if self.options['type'] == TimeWarpingType.PLOT:
            dtw_result: DTW = dtw(query, reference)
            data = DataFrame(
                {
                    f'tw_{columns[0]}': query[warp(dtw_result, index_reference=False)],
                    f'tw_{columns[1]}': reference[warp(dtw_result, index_reference=True)],
                },
            )
        elif self.options['type'] == TimeWarpingType.DISTANCE:
            dtw_result: DTW = dtw(query, reference, distance_only=True)
            data = DataFrame([{'tw_distance': dtw_result.normalizedDistance}])

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
