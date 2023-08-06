from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class RandomForest(BaseMethod):
    """
    For now its only useful for feature importances
    """
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        random_forest = RandomForestClassifier()
        random_forest.fit(numeric_part, input_data['group'])

        columns = numeric_part.columns
        feature_importances = random_forest.feature_importances_
        data = DataFrame(
            [{columns[i]: feature_importances[i] for i in range(len(columns))}],
        )

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'group') and not DataFrameUtils.decompose(input_data)[0].empty
