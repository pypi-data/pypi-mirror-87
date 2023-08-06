from datetime import datetime
from matplotlib import pyplot as plt

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import INIT_DATA

print(INIT_DATA)


class TestSeasonalDecomposition:
    def test(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance ->
        seasonal decomposition
        """
        data = Pipeline([
            FilterByDate({
                'gte': datetime(2020, 10, 10, 10, 10),
            }),
            # Selector({
            #     'exclude': ['x'],
            # }),
            Group({
                'keys': ['instance'],
            }),
            SeasonalDecomposition({
                'period': 60 * 24 // 30,
            }),
            Group({
                'keys': ['instance'],
            }),
            Normalisation({
                'type': 'min_max',
            }),
        ]).run(INIT_DATA)

        assert not data['error']
        data = data['data']

        INIT_DATA.groupby('instance').plot(x='date', y=['feature_0', 'feature_1'])
        data.groupby('instance').plot(x='date', y=['feature_0', 'feature_1'])
        plt.show()


TestSeasonalDecomposition().test()
