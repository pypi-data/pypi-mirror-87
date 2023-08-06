import pandas as pd
from matplotlib import pyplot as plt

from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.groups import Group
from ds_methods.methods.preprocessing import Resampling

from ds_methods.methods.custom import KSTestOnAverageDay

from ds_methods.templates.init_data import load_raw_data

pd.set_option('display.max_rows', 100)


data = load_raw_data()

data = Group({'keys': ['target']})\
    .make(data)['data']\
    .apply(lambda group: Resampling({'rule': '4Min'})\
    .make(group)['data'])\
    .reset_index(drop=True)

ks = KSTestOnAverageDay({'time': 2}).make(data)['data']

columns = ['area', 'size', 'temperature']
for name, group in ks.groupby('target'):
    day_groups = Group({'time': 24}).make(group)['data']

    dates = []
    for day, day_group in day_groups:
        if not day_group.empty:
            dates.append([day_group.index[0], day.date()])

    for column in columns:
        _, axes = plt.subplots(2, figsize=(14, 12))

        p_values = group[f'{column}_ks_p_value']
        p_values[group[f'{column}_ks_p_value'] <= 0.05] = 0
        p_values[group[f'{column}_ks_p_value'] > 0.05] = 1

        group[column].plot(ax=axes[0], linewidth=0.75, alpha=0.75)
        group[f'{column}_ks_average_day'].plot(ax=axes[0], linewidth=0.75, alpha=0.75)
        p_values.plot(ax=axes[1], linewidth=3, alpha=0.85)

        axes[0].set_xticks([])
        # axes[0].set_xticks(list(zip(*dates))[0])
        # axes[0].set_xticklabels(list(zip(*dates))[1], rotation=30)
        axes[1].set_xticks(list(zip(*dates))[0])
        axes[1].set_xticklabels(list(zip(*dates))[1], rotation=30)

        axes[0].set_title(f'KS-Test with rounded p-value\nMouse - {name}, Feature - {column}')

        axes[0].legend([column, f'{column}_ks_average_day'], loc=1)
        axes[1].legend([f'{column}_ks_rounded_p_value'], loc=1)
        plt.xlabel('date')

        plt.show()
