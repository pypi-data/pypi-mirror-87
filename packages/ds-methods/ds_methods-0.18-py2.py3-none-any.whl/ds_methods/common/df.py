from typing import Dict, List, Tuple
from numbers import Number
import pandas as pd
import numpy as np
from pandas import DataFrame, Series

from .constants import MIN_ROWS_FOR_ACC


class DataFrameUtils:
    @staticmethod
    def get_query_value(value) -> str:
        if not isinstance(value, Number):
            return f"'{value}'"

        return f"{value}"

    @staticmethod
    def compose_query(options: Dict[str, Dict]) -> str:
        filters = []
        for key in options:
            key_options = options[key]
            if 'equal' in key_options:
                filters.append(f"{key} == {DataFrameUtils.get_query_value(key_options['equal'])}")
            else:
                if 'gte' in key_options:
                    filters.append(f"{key} >= {DataFrameUtils.get_query_value(key_options['gte'])}")
                if 'lte' in key_options:
                    filters.append(f"{key} <= {DataFrameUtils.get_query_value(key_options['lte'])}")

        return ' and '.join(filters)

    @staticmethod
    def eval_query(input_data: DataFrame, query: str) -> DataFrame:
        """
        'python' engine is faster for a small data
        """
        if len(input_data.index) < MIN_ROWS_FOR_ACC:
            return input_data.query(query, engine='python')

        return input_data.query(query)

    @staticmethod
    def concatenate(parts: List[DataFrame]) -> DataFrame:
        return pd.concat(
            [part.reset_index(drop=True) for part in parts],
            sort=False,
            axis='columns',
            copy=False,
        ).dropna(how='all').reset_index(drop=True)

    @staticmethod
    def decompose(input_data: DataFrame, include: List[str] = None) -> Tuple[DataFrame, DataFrame]:
        if not include:
            include = ['number']

        return input_data.select_dtypes(include=include), input_data.select_dtypes(exclude=include)

    @staticmethod
    def fillna(input_data: DataFrame) -> DataFrame:
        data = input_data.copy()
        numeric_part, other_part = DataFrameUtils.decompose(data)
        data[numeric_part.columns] = data[numeric_part.columns].fillna(0)
        data[other_part.columns] = data[other_part.columns].fillna('')

        return data

    @staticmethod
    def repeat_rows(input_data: DataFrame, n_repeat: int) -> DataFrame:
        return input_data.loc[input_data.index.repeat(n_repeat)].reset_index(drop=True)

    @staticmethod
    def categorize_values(values: iter, categories: list = None) -> [int]:
        if categories is None:
            categories = [value for value in np.unique(values) if value]

        return [
            categories.index(value) if value in categories else -1
            for value in values
        ]

    @staticmethod
    def concatenate_columns(input_data: DataFrame, delimeter=None, column_type=str) -> Series:
        columns = input_data.columns
        result = input_data[columns[0]].astype(column_type)

        for column in columns[1:]:
            if delimeter:
                result += delimeter
            result += input_data[column].astype(column_type)

        return result

    @staticmethod
    def apply_function(input_data: DataFrame, method) -> DataFrame:
        data = method.make(input_data)
        if data['error']:
            raise Exception(data['error'])

        return data['data']
