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


class TestKMeans:
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
        KMeans
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
                'time': 24,
            }),
            Basic({
                'method': 'mean',
            }),
            KMeans({
                'clusters': 5,
            }),
            PCA({
                'components': 2,
            }),
        ]).run(INIT_DATA)

        print(data['error'])
        assert not data['error']
        data = data['data']

        print(data.groupby('instance').head(5))
        # INIT_DATA.groupby('instance').plot(x='date', y=['feature_0', 'feature_2', 'feature_5', 'feature_8'])
        data.plot.scatter(x=data.columns[0], y=data.columns[0], c=categories_to_colors(data['cluster']))
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
        KMeans
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
                'period': 24 * 60 // 30,
            }),
            Group({
                'keys': ['instance'],
            }),
            Basic({
                'method': 'mean',
            }),
            KMeans({
                'clusters': 2,
            }),
            PCA({
                'components': 2,
            }),
        ]).run(INIT_DATA)

        print(data['error'])
        assert not data['error']
        data = data['data']

        # INIT_DATA.groupby('instance').plot(x='date', y=['feature_0', 'feature_2', 'feature_5', 'feature_8'])
        data.plot.scatter(x=data.columns[0], y=data.columns[0], c=categories_to_colors(data['cluster']))
        plt.show()


TestKMeans().test_days()
# TestKMeans().test_mice()
