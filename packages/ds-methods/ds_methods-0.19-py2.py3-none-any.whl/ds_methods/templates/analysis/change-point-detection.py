import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import ruptures as rpt

from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *

from ds_methods.common.df import DataFrameUtils

from ds_methods.templates.init_data import load_raw_data

data = load_raw_data()

data = Group({'keys': ['target']})\
    .make(data)['data']\
    .apply(lambda group: Resampling({'rule': '4Min'})\
    .make(group)['data'])\
    .reset_index(drop=True)

numeric_part, _ = DataFrameUtils.decompose(data)

windows = [15 * 6]
# Checking correct window size for change point detection

columns = ['area', 'size', 'temperature']
for name, group in data.groupby('target'):
    for window in windows:
        group = MovingAverage({'window': window}).make(group)['data'].dropna()
        day_groups = group.groupby(pd.Grouper(freq='24H', key='date'))
        dates = []
        for day, day_group in day_groups:
            if not day_group.empty:
                dates.append([day_group.index[0], day.date()])

        if len(dates) >= 7:
            group = group[group['date'].dt.date < dates[-3][1]]
            dates = dates[:-3]

        for column in columns:
            points = group[column].to_numpy()

            # Change point detection with the Pelt search method
            # model = "rbf"
            # algo = rpt.Pelt(model=model).fit(points)
            # result = algo.predict(pen=10)
            # rpt.display(points, result, figsize=(14, 12))
            #
            # plt.title(f'Pelt Search Method,\nMouse - {name}, Feature - {column}, Widnow - {window}')
            # plt.xticks(
            #     *zip(*dates),
            #     rotation=30,
            # )
            # plt.ylabel(column)
            # plt.xlabel('date')
            #
            # plt.show()

            # # Change point detection with the Binary Segmentation search method
            # model = "l2"
            # algo = rpt.Binseg(model=model).fit(points)
            # result = algo.predict(n_bkps=10)
            # # show results
            # rpt.show.display(points, result, figsize=(14, 12))
            # plt.title(f'Binary Segmentation Search Method,\nMouse - {name}, Feature - {column}, Widnow - {window}')
            # plt.show()

            # Change point detection with window-based search method
            model = "l2"
            print(name, column, window, points, len(points))
            algo = rpt.Window(width=15, model=model).fit(points)
            result = algo.predict(n_bkps=4)[:1] + [len(points) - 1]
            print(result)
            rpt.show.display(points, result, figsize=(14, 12))

            plt.title(f'Window-Based Search Method,\nMouse - {name}, Feature - {column}')
            plt.xticks(
                *zip(*dates),
                rotation=30,
            )
            plt.ylabel(column)
            plt.xlabel('date')

            plt.show()
