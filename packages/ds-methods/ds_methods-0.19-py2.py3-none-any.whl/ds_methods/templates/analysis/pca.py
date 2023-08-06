from matplotlib import pyplot as plt
import seaborn as sns

from ds_methods.common.utils import categories_to_colors
from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import load_raw_data

data = load_raw_data()

data = Group({'keys': ['target']})\
    .make(data)['data']\
    .apply(lambda group: Resampling({'rule': '4Min'})\
    .make(group)['data'])\
    .reset_index(drop=True)

pca_group_time = 3
#
# data = Pipeline([
#     Group({
#         'keys': ['target'],
#     }),
#     Normalisation({
#         'type': 'z_score',
#     }),
#     Group({
#         'keys': ['target'],
#     }),
#     SeasonalDecomposition({
#         'period': 60 * 24 // 4,
#     }),
#     Group({
#         'keys': ['target'],
#         'time': pca_group_time,
#     }),
#     Basic({
#         'method': 'mean',
#     }),
# ]).run(data)['data']
#
#
# data = PCA({
#     'components': 2,
# }).make(data.dropna())['data']
#
# _, ax = plt.subplots(figsize=(12, 12))
#
# sns.scatterplot(data=data, hue='condition', x=data.columns[0], y=data.columns[1], s=100)
# plt.legend(loc=2)
# plt.title(f'PCA for all mice, by {pca_group_time} hours, colored by condition\n'
#           'Z-Score norm. -> SD')
#
# plt.show()

for name, group in data.groupby('group'):
    group = Pipeline([
        Group({
            'keys': ['target'],
        }),
        Normalisation({
            'type': 'z_score',
        }),
        Group({
            'keys': ['target'],
        }),
        SeasonalDecomposition({
            'period': 60 * 24 // 4,
        }),
        Group({
            'keys': ['target'],
            'time': pca_group_time,
        }),
        Basic({
            'method': 'mean',
        }),
        PCA({
            'components': 2,
        }),
    ]).run(group)['data']

    _, ax = plt.subplots(figsize=(12, 12))

    sns.scatterplot(data=group, hue='condition', x=group.columns[0], y=group.columns[1], s=100)

    plt.legend(loc=2)
    plt.title(f'PCA for {name} mice, by {pca_group_time} hours, colored by condition\n'
              'Z-Score norm. -> SD')

    plt.show()
