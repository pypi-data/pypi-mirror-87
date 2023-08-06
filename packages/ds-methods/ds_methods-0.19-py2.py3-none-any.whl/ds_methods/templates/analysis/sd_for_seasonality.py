import numpy as np
from matplotlib import pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling

from ds_methods.templates.init_data import load_raw_data


data = load_raw_data()

data = Group({'keys': ['target']})\
    .make(data)['data']\
    .apply(lambda group: Resampling({'rule': '4Min'})\
    .make(group)['data'])\
    .reset_index(drop=True)

print(data)

period = 24 * 60 // 4
period_days = 2

columns = ['area', 'size', 'temperature']
for name, group in data.groupby('target'):
    if name in ['27']:
        numeric_part, other_part = DataFrameUtils.decompose(group)

        day_groups = Group({'time': 24}).make(group)['data']

        dates = []
        for day, day_group in day_groups:
            if not day_group.empty:
                dates.append([day_group.index[0], day.date()])

        for column in columns:
            global_sd = seasonal_decompose(group[column], period=period, extrapolate_trend=False)
            seasonals = {}

            healthy_seasonality = seasonal_decompose(
                group[column][:3*period],
                period=period,
                extrapolate_trend=False,
            ).seasonal[:period].to_numpy()

            for additional_day in range(period_days, len(group) // period + 1):
                day = group['date'].iloc[additional_day * period].date()
                sd = seasonal_decompose(
                    group[column][(additional_day - period_days) * period: additional_day * period],
                    period=period,
                    extrapolate_trend=False,
                )
                seasonals[day] = sd.seasonal[:period].to_numpy()

            _, axes = plt.subplots(2, figsize=(14, 12))

            legends = []
            distances = [0.] * period_days
            for index, (day, seasonal) in enumerate(seasonals.items()):
                distances.append(np.linalg.norm(seasonal - healthy_seasonality))

            axes[0].plot(group[column], linewidth=2, alpha=0.8)
            axes[0].plot(global_sd.trend, linewidth=3, alpha=1)
            axes[1].plot(distances, linewidth=3, alpha=1)

            axes[0].set_title(f'Distance between current and previous days SD Seasonality\nMouse - {name}, Feature - {column}')

            axes[0].legend(['raw', 'trend'])
            axes[0].set_xticks(list(zip(*dates))[0])
            axes[0].set_xticklabels(list(zip(*dates))[1], rotation=30)

            axes[1].set_xticks(range(len(dates)))
            axes[1].set_xticklabels(list(zip(*dates))[1], rotation=30)

            plt.ylabel(column + ' seasonality distance')
            plt.xlabel('date')
            plt.legend(legends)

            plt.savefig(f'plots/{name}_{column}.png')

            # plt.show()
