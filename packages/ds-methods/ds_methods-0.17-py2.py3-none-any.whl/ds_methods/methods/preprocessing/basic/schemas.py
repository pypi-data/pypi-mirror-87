from schema import Schema, And, Use, Or, Optional

from ds_methods.common.enums import BaseEnum


class BasicMethod(BaseEnum):
    MIN = 'min'
    MAX = 'max'
    MEAN = 'mean'
    MEDIAN = 'median'
    STD = 'std'
    IQR = 'iqr'


options_schema = Schema(
    {
        'method': And(
            str,
            lambda x: BasicMethod.validate(x),
        ),
    },
    ignore_extra_keys=True,
)
