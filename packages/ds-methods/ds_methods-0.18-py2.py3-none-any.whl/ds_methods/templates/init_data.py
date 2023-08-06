from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.cm as cm

pd.set_option('mode.chained_assignment', None)


POINTS_RANGE = (1000, 5000)
N_GROUPS = 3
N_INSTANCES = 10
N_FEATURES = 10
COLORS = cm.rainbow(np.linspace(0, 1, N_INSTANCES))


def load_raw_data(is_full=False):
    data = pd.read_csv('./mica_data.csv' if is_full else './mica_data_100.csv')
    data['date'] = pd.to_datetime(data['date'], utc=True).dt.tz_localize(None)
    data = data[data['date'] >= datetime(2020, 11, 1)]
    data['condition'] = data['is_sick'].copy()
    data['condition'][~data['is_sick']] = 'healthy'
    data['condition'][data['is_sick']] = 'infected'

    data['group'][data['target'] <= 27] = 'Group 0'
    data['group'][data['target'] > 27] = 'Group 1'

    data['target'] = data['target'].astype(str)

    data = data.drop(['is_sick', 'row'], axis=1)

    return data


def make_fake_data(
        points_range=POINTS_RANGE,
        n_groups=N_GROUPS,
        n_instances=N_INSTANCES,
        n_features=N_FEATURES,
        colors=COLORS,
):
    data = []
    for instance in range(n_instances):
        features = []
        n_points = np.random.randint(*points_range)
        dates = pd.date_range(
            datetime(2020, 10, 10, 1, 00),
            periods=n_points,
            freq='27min',
        )
        linespace = np.linspace(0, 10 * np.pi, n_points)
        for feature in range(n_features):
            func = np.sin if feature % 2 else np.cos
            noise = np.random.random(n_points)
            features.append(
                func(linespace) * noise + 0.1 * noise,
            )

        for sample in range(n_points):
            data.append({
                'instance': f'instance_{instance}',
                'group': f'group_{instance % n_groups}',
                'date': dates[sample],
                'state': 'healthy' if sample <= n_points // 2 else 'sick',
                **{
                    f'feature_{feature}': features[feature][sample]
                    for feature in range(n_features)
                },
            })

    return pd.DataFrame(data)

# INIT_DATA = make_fake_data()
