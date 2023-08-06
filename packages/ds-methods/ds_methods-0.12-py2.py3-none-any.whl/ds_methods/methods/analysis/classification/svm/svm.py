from pandas import DataFrame
from sklearn.svm import SVC

from ds_methods.common.validators import check_keys
from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class SVM(BaseMethod):
    """
    For now its only useful for feature importances (=> only linear kernel)
    """
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        svm = SVC(kernel='linear')
        svm.fit(numeric_part, input_data['group'])

        columns = numeric_part.columns
        feature_importances = svm.coef_[0]
        data = DataFrame(
            [{columns[i]: feature_importances[i] for i in range(len(columns))}],
        )

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, 'group') and not DataFrameUtils.decompose(input_data)[0].empty
