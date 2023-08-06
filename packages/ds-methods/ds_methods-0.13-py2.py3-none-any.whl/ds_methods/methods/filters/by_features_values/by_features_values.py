from pandas import DataFrame

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema, MATCHERS


class FilterByFeaturesValues(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:

        return MethodOutput(
            data=DataFrameUtils.eval_query(
                input_data,
                DataFrameUtils.compose_query(self.options),
            ),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        self.options = self.transform_options()

        return check_keys(input_data, self.options.keys())

    def transform_options(self):
        result = {}
        for feature in self.options:
            for key, matcher in MATCHERS.items():
                if matcher(feature):
                    feature_name = feature[:-(2 + len(key))]
                    if feature_name in result:
                        result[feature_name][key] = self.options[feature]
                    else:
                        result[feature_name] = {key: self.options[feature]}

        return result
