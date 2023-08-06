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


class TestPCA:
    def test_days(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance->
        seasonal decomposition ->
        group by instance and by 24hours ->
        average ->
        PCA
        """
        data = Pipeline([
            FilterByDate({
                'gte': datetime(2020, 10, 10, 10, 10),
            }),
            Selector({
                'exclude': ['feature_0'],
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
                'time': 24,
            }),
            Basic({
                'method': 'mean',
            }),
            PCA({
                'components': 2,
            }),
        ]).run(INIT_DATA)

        assert not data['error']
        data = data['data']

        INIT_DATA.groupby('instance').plot(x='date', y=['feature_1', 'feature_2'])
        data.plot.scatter(x=data.columns[0], y=data.columns[1], c=categories_to_colors(data['group']))
        plt.show()

    def test_mice(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance ->
        seasonal decomposition ->
        group by instance ->
        average ->
        PCA
        """
        data = Pipeline([
            FilterByDate({
                'gte': datetime(2020, 10, 10, 10, 10),
            }),
            Selector({
                'exclude': ['feature_0'],
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
            }),
            Basic({
                'method': 'mean',
            }),
            PCA({
                'components': 2,
            }),
        ]).run(INIT_DATA)

        assert not data['error']
        data = data['data']

        INIT_DATA.groupby('instance').plot(x='date', y=['feature_1', 'feature_2'])
        data.plot.scatter(x=data.columns[0], y=data.columns[1], c=categories_to_colors(data['group']))
        plt.show()


TestPCA().test_days()
TestPCA().test_mice()
