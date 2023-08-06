from pandas import DataFrame

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput
from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.groups import Group
from ds_methods.methods.base import BaseMethod
from ds_methods.methods.analysis import KSTest

from ds_methods.methods.custom import AverageDay

from .schemas import options_schema


class KSTestOnAverageDay(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        target_groups = Group({'keys': ['target']}).make(input_data)['data']

        ks_tests = {}
        for target, group in target_groups:
            print(target)
            average_healthy_day = AverageDay({}).make(group[group['condition'] == 'healthy'])['data']
            day_groups = Group({'time': 24}).make(group)['data']
            numeric_columns = average_healthy_day.select_dtypes(['number'])

            for column in numeric_columns:
                duplicated_average_healthy_day = []
                for day, day_group in day_groups:
                    duplicated_average_healthy_day += list(average_healthy_day[column][
                        average_healthy_day['times'].isin(day_group['date'].dt.time)
                    ])

                if f'{column}_ks_p_value' not in ks_tests:
                    ks_tests[f'{column}_ks_average_day'] = []
                    ks_tests[f'{column}_ks_p_value'] = []
                    ks_tests[f'{column}_ks_statistic'] = []

                ks_test_input = Group({'time': self.options['time']}).make(
                    DataFrame({
                        'date': group['date'],
                        'source': duplicated_average_healthy_day,
                        'query': group[column],
                    }),
                )['data']

                ks_test = ks_test_input.apply(
                    lambda x: KSTest({
                        'columns': ['source', 'query'],
                    }).make(x)['data'],
                ).reset_index(drop=True).fillna(method='ffill')

                ks_tests[f'{column}_ks_average_day'] += list(duplicated_average_healthy_day)
                ks_tests[f'{column}_ks_p_value'] += list(ks_test['p_value'])
                ks_tests[f'{column}_ks_statistic'] += list(ks_test['statistic'])

        ks_tests = DataFrame(ks_tests)

        return MethodOutput(
            data=DataFrameUtils.concatenate([input_data, ks_tests]),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, ['date', 'condition']) and check_datetime(input_data['date'])
