from schema import Schema, And

from ds_methods.common.enums import BaseEnum


class TimeWarpingType(BaseEnum):
    PLOT = 'plot'
    DISTANCE = 'distance'


options_schema = Schema(
    {
        'columns': [str, str],
        'type': And(str, lambda x: TimeWarpingType.validate(x)),
    },
    ignore_extra_keys=True,
)
