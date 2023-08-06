from pandas import DataFrame
from hmmlearn.hmm import GaussianHMM

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class HMM(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)
        group_sizes = input_data.groupby('group').size().to_numpy()
        hmm = GaussianHMM(n_components=self.options['components'])
        hmm.fit(numeric_part, group_sizes)
        predictions = hmm.predict(numeric_part, group_sizes)

        data = DataFrame(
            predictions,
            columns=['hmm_state'],
        )
        data = DataFrameUtils.concatenate([data, numeric_part, other_part])

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return self.options['components'] <= len(input_data.index) and check_keys(input_data, 'group')
