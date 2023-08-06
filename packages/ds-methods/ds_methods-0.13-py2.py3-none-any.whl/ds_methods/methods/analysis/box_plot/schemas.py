from schema import Schema, And

from ds_methods.common.enums import BaseEnum


class BoxPlotType(BaseEnum):
    FEATURES = 'features'
    DAYS = 'days'


options_schema = Schema(
    {'type': And(str, lambda x: BoxPlotType.validate(x))},
    ignore_extra_keys=True,
)
