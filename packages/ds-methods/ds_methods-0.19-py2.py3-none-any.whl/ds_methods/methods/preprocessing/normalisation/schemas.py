from schema import Schema, And

from ds_methods.common.enums import BaseEnum


class NormalisationType(BaseEnum):
    MIN_MAX = 'min_max'
    MEAN = 'mean'
    Z_SCORE = 'z_score'


options_schema = Schema(
    {'type': And(str, lambda x: NormalisationType.validate(x))},
    ignore_extra_keys=True,
)
