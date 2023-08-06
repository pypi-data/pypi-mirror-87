from pandas import DataFrame

from sklearn.linear_model import LinearRegression

from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput
from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.groups import Group
from ds_methods.methods.base import BaseMethod
from ds_methods.methods.analysis import TimeWarping, TimeWarpingType

from ds_methods.methods.custom import AverageDay

from .schemas import options_schema


class TimeWarpingOnRegression(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        target_groups = Group({'keys': ['target']}).make(input_data)['data']

        common_average_healthy_day = AverageDay({}).make(input_data[input_data['condition'] == 'healthy'])['data']

        regressions = {}
        time_warpings = {}
        for target, group in target_groups:
            day_groups = Group({'time': 24}).make(group)['data']

            target_average_healthy_day = AverageDay({}).make(group[group['condition'] == 'healthy'])['data']
            numeric_columns = target_average_healthy_day.select_dtypes(['number'])
            for column in numeric_columns:
                model = LinearRegression()
                model.fit(
                    common_average_healthy_day[column].to_numpy().reshape(-1, 1),
                    target_average_healthy_day[column],

                )
                if f'{column}_regression' not in regressions:
                    regressions[f'{column}_regression'] = []
                if f'{column}_tw_distance' not in time_warpings:
                    time_warpings[f'{column}_tw_distance'] = []

                regression = model.predict(common_average_healthy_day[column].to_numpy().reshape(-1, 1))

                duplicated_regression = []
                for day, day_group in day_groups:
                    duplicated_regression += list(regression[
                        target_average_healthy_day['times'].isin(day_group['date'].dt.time)
                    ])

                regressions[f'{column}_regression'] += duplicated_regression

                tw_input = Group({'time': self.options['time']}).make(
                    DataFrame({'date': group['date'], 'query': duplicated_regression, 'source': group[column]}),
                )['data']
                tw = tw_input.apply(
                    lambda x: TimeWarping({
                        'columns': ['source', 'query'],
                        'type': TimeWarpingType.DISTANCE,
                    }).make(x)['data'],
                ).reset_index(drop=True).fillna(method='ffill')

                time_warpings[f'{column}_tw_distance'] += list(tw['tw_distance'])

        regressions = DataFrame(regressions)
        time_warpings = DataFrame(time_warpings)

        return MethodOutput(
            data=DataFrameUtils.concatenate([input_data, regressions, time_warpings]),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        return check_keys(input_data, ['date', 'condition']) and check_datetime(input_data['date'])
