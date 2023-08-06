from datetime import datetime
from matplotlib import pyplot as plt

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import INIT_DATA

print(INIT_DATA)


class TestKSTest:
    def test(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance->
        seasonal decomposition ->
        group by instance and by 24hours ->
        KSTest
        """
        processed_data = Pipeline([
            FilterByDate({
                'gte': datetime(2020, 10, 10, 10, 00),
            }),
            Selector({
                'exclude': ['feature_3', 'feature_9'],
            }),
            Group({
                'keys': ['instance'],
            }),
            Normalisation({
                'type': 'min_max',
            }),
            Group({
                'keys': ['instance'],
            }),
            SeasonalDecomposition({
                'period': 60 * 24 // 15,
            }),
        ]).run(INIT_DATA)

        assert not processed_data['error']
        processed_data = processed_data['data']

        ks_test_columns = ['feature_0', 'feature_1']
        data = Pipeline([
            Group({
                'keys': ['instance'],
                'time': 4,
            }),
            KSTest({
                'columns': ks_test_columns,
            }),
            FilterByFeaturesValues({
               'p_value': {'lte': 0.1},
            }),
        ]).run(processed_data)

        assert not data['error']
        data = data['data']
        print(data)

        plt.figure(figsize=(12, 10))

        plt.plot(
            INIT_DATA[INIT_DATA['instance'] == 'instance_0']['date'],
            INIT_DATA[INIT_DATA['instance'] == 'instance_0'][ks_test_columns[0]],
            label=ks_test_columns[0],
        )
        plt.plot(
            INIT_DATA[INIT_DATA['instance'] == 'instance_0']['date'],
            INIT_DATA[INIT_DATA['instance'] == 'instance_0'][ks_test_columns[1]],
            label=ks_test_columns[1],
        )
        plt.plot(
            processed_data[processed_data['instance'] == 'instance_0']['date'],
            processed_data[processed_data['instance'] == 'instance_0'][ks_test_columns[0]],
            label='processed ' + ks_test_columns[0],
        )
        plt.plot(
            processed_data[processed_data['instance'] == 'instance_0']['date'],
            processed_data[processed_data['instance'] == 'instance_0'][ks_test_columns[1]],
            label='processed ' + ks_test_columns[1],
        )
        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0']['p_value'],
            label='p_value',
        )
        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0']['statistic'],
            label='statistic',
        )

        plt.legend()
        plt.show()


TestKSTest().test()
