from datetime import datetime
from matplotlib import pyplot as plt

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import INIT_DATA

print(INIT_DATA)


class TestTimeWarping:
    def test_plot(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance->
        seasonal decomposition ->
        TimeWarping
        """
        tw_columns = ['feature_0', 'feature_1']
        data = Pipeline([
            FilterByDate({
                'gte': datetime(2020, 10, 10, 10, 00),
                'lte': datetime(2022, 10, 10, 10, 00),
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
            Group({
                'keys': ['instance'],
            }),
            TimeWarping({
                'columns': tw_columns,
                'type': 'plot',
            }),
        ]).run(INIT_DATA)

        assert not data['error']
        data = data['data']
        print(data)

        plt.figure(figsize=(14, 12))

        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0'][f'tw_{tw_columns[0]}'],
            label=f'tw_{tw_columns[0]}',
            linewidth=8,
            alpha=0.8,
        )
        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0'][f'tw_{tw_columns[1]}'],
            label=f'tw_{tw_columns[1]}',
            linewidth=8,
            alpha=0.8,
        )
        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0'][tw_columns[0]],
            label='processed ' + tw_columns[0],
            linewidth=4,
            linestyle='--',
        )
        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0'][tw_columns[1]],
            label='processed ' + tw_columns[1],
            linewidth=4,
            linestyle='--',
        )
        plt.plot(
            INIT_DATA[INIT_DATA['instance'] == 'instance_0']['date'],
            INIT_DATA[INIT_DATA['instance'] == 'instance_0'][tw_columns[0]],
            label=tw_columns[0],
            alpha=0.3,
        )
        plt.plot(
            INIT_DATA[INIT_DATA['instance'] == 'instance_0']['date'],
            INIT_DATA[INIT_DATA['instance'] == 'instance_0'][tw_columns[1]],
            label=tw_columns[1],
            alpha=0.3,
        )

        plt.legend()
        plt.show()

    def test_distance(self):
        """
        INIT_DATA ->
        filter by date ->
        group by instance ->
        normalisation ->
        group by instance ->
        seasonal decomposition ->
        group by instance and by hours ->
        TimeWarping
        """
        tw_columns = ['feature_0', 'feature_1']
        data = Pipeline([
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
            Group({
                'keys': ['instance'],
                'time': 24,
            }),
            TimeWarping({
                'columns': tw_columns,
                'type': 'distance',
            }),
        ]).run(INIT_DATA)

        assert not data['error']
        data = data['data']
        print(data)

        plt.figure(figsize=(14, 12))

        plt.plot(
            INIT_DATA[INIT_DATA['instance'] == 'instance_0']['date'],
            INIT_DATA[INIT_DATA['instance'] == 'instance_0'][tw_columns[0]],
            label=tw_columns[0],
            alpha=0.8,
        )
        plt.plot(
            INIT_DATA[INIT_DATA['instance'] == 'instance_0']['date'],
            INIT_DATA[INIT_DATA['instance'] == 'instance_0'][tw_columns[1]],
            label=tw_columns[1],
            alpha=0.8,
        )
        plt.plot(
            data[data['instance'] == 'instance_0']['date'],
            data[data['instance'] == 'instance_0']['tw_distance'],
            label='tw_distance',
            linewidth=5,
        )

        plt.legend()
        plt.show()


TestTimeWarping().test_plot()
TestTimeWarping().test_distance()
