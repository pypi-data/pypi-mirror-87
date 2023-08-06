from schema import Schema, Optional, And


options_schema = Schema(
    {Optional('time', default=1): And(int, lambda x: x >= 1)},
    ignore_extra_keys=True,
)
