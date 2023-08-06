from pandas import DataFrame
from sklearn.cluster import KMeans as sklearnKMeans

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class KMeans(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        n_clusters = self.options['clusters']
        k_means = sklearnKMeans(n_clusters=n_clusters)
        k_means.fit(numeric_part)

        data = DataFrame(
            k_means.labels_,
            columns=['cluster'],
        )
        data = DataFrameUtils.concatenate([numeric_part, data, other_part])

        return MethodOutput(
            data=data,
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return self.options['clusters'] <= len(input_data.index)
