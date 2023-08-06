from schema import Schema, And, Or, Optional

from ds_methods.common.enums import BaseEnum


class JoinHows(BaseEnum):
    Left = 'left'
    Right = 'right'
    Outer = 'outer'
    Inner = 'inner'


options_schema = Schema(
    {
        Optional('on', default=None): Or(str, [str]),
        Optional('left_on', default=None): Or(str, [str]),
        Optional('right_on', default=None): Or(str, [str]),
        Optional('how', default=JoinHows.Inner): And(str, lambda x: JoinHows.validate(x)),
        Optional('is_drop_merged', default=True): bool,
    },
    ignore_extra_keys=True,
)
