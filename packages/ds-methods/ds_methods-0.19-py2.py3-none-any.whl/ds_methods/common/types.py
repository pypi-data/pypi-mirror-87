from typing import Optional, TypedDict
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy


class MethodOutput(TypedDict):
    error: Optional[str]
    data: Optional[DataFrame]


class GroupMethodOutput(TypedDict):
    error: Optional[str]
    data: Optional[DataFrameGroupBy]
