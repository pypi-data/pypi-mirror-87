from datetime import datetime
from matplotlib import pyplot as plt

from ds_methods.common.utils import categories_to_colors
from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import INIT_DATA

print(INIT_DATA)


class TestHMM:
    def test(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance->
        seasonal decomposition ->
        group by instance and by 24hours ->
        average ->
        HMM
        """
        data = Pipeline([
            FilterByDate({
                'gte': datetime(2020, 10, 10, 10, 10),
            }),
            Selector({
                'exclude': ['feature_0', 'feature_9'],
            }),
            Group({
                'keys': ['instance'],
            }),
            Normalisation({
                'type': 'z_score',
            }),
            Group({
                'keys': ['instance'],
            }),
            SeasonalDecomposition({
                'period': 60 * 24 // 30,
            }),
            Group({
                'keys': ['instance'],
                'time': 3,
            }),
            Basic({
                'method': 'mean',
            }),
            HMM({
                'components': 3,
            }),
        ]).run(INIT_DATA)

        print(data['error'])
        assert not data['error']

        data = data['data']
        print(data)

        fig, ax = plt.subplots(figsize=(15, 7))
        for _, group in data.groupby('instance'):
            group.plot.scatter(x='date', y='feature_1', ax=ax, c=categories_to_colors(group['hmm_state']))
        plt.show()


TestHMM().test()
