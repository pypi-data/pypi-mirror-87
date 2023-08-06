import pandas as pd
from matplotlib import pyplot as plt

from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.groups import Group
from ds_methods.methods.preprocessing import Resampling

from ds_methods.methods.custom import AverageDay

from ds_methods.templates.init_data import load_raw_data


data = load_raw_data()

_, ax = plt.subplots(figsize=(14, 12))
_, avg_ax = plt.subplots(figsize=(14, 12))
legends = []
columns = ['temperature']
for name, group in data.groupby('target'):
    if name in ['25']:
        numeric_part, other_part = DataFrameUtils.decompose(group)
        group = Resampling({'rule': '2Min'}).make(group)['data']
        day_groups = Group({'time': 24}).make(group)['data']

        print(group)

        average_healthy_day = AverageDay({}).make(group[group['condition'] == 'healthy'])['data']
        duplicated_average_healthy_day = pd.DataFrame()
        for day, day_group in day_groups:
            duplicated_average_healthy_day = pd.concat([
                duplicated_average_healthy_day.copy(),
                average_healthy_day[
                    average_healthy_day['times'].isin(day_group['date'].dt.time)
                ],
            ], axis=0).reset_index(drop=True)

        print(duplicated_average_healthy_day)

        for column in columns:
            group.plot(y=columns, ax=ax, linewidth=0.75, alpha=0.75)
            duplicated_average_healthy_day.plot(y=columns, ax=ax, linewidth=1, alpha=0.75)
            legends.append(f'Avg. Mouse: {name}, Feature: {column}')

plt.title('Plot')
plt.xlabel('date')
plt.legend(legends)

plt.show()
