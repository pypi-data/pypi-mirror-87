from datetime import datetime

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import INIT_DATA

print(INIT_DATA)


class TestSVM:
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
        SVM
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
            SVM({
            }),
        ]).run(INIT_DATA)

        print(data['error'])
        assert not data['error']
        data = data['data']

        print(data)


TestSVM().test()
