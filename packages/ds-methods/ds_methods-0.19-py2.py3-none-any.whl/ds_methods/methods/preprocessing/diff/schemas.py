from schema import Schema, And


options_schema = Schema(
    {'periods': And(int, lambda x: x >= 1)},
    ignore_extra_keys=True,
)
