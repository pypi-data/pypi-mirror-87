from typing import Iterable
import numpy as np
import matplotlib.cm as cm


def categories_to_colors(categories: Iterable) -> [[float, float, float]]:
    unique_categories = list(set(categories))
    colors = cm.rainbow(np.linspace(0, 1, len(unique_categories)))

    return [
        colors[unique_categories.index(category)]
        for category in categories
    ]
