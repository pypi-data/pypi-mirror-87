from typing import List
from pandas import DataFrame
from sklearn.decomposition import PCA as sklearnPCA

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class PCA(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        pca = sklearnPCA(n_components=self.options['components'])
        pca.fit(numeric_part)

        data = DataFrame(
            pca.transform(numeric_part),
            columns=PCA.make_pca_column_names(pca.explained_variance_ratio_),
        )
        data = DataFrameUtils.concatenate([data, numeric_part, other_part])

        return MethodOutput(
            data=data,
            error=None,
        )

    @staticmethod
    def make_pca_column_names(variance_ratios: List[float]) -> List[str]:
        """
        example: ['PCA1_(67%)', 'PCA2_(33%)']
        """
        return [
            'PCA%i_(%s%%)' % (i, int(ratio * 100))
            for i, ratio in enumerate(variance_ratios, 1)
        ]

    def validate_input_(self, input_data: DataFrame) -> bool:
        return self.options['components'] <= len(input_data.columns)
