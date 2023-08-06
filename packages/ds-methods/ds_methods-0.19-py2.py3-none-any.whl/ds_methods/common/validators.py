from typing import List
from pandas import DataFrame
from pandas.api.types import is_datetime64_any_dtype as is_datetime


def check_keys(input_data: DataFrame, keys=str or List[str]) -> bool:
    """
    Check if input data contains 'keys' keys
    :param input_data: DataFrame
    :param keys: str or List[str]
    :return: bool
    """
    if isinstance(keys, str):
        return keys in input_data

    return set(keys).issubset(input_data.columns)


def check_datetime(column: DataFrame.columns) -> bool:
    return is_datetime(column)
