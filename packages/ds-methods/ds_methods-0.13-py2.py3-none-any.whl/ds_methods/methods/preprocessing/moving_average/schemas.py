from schema import Schema, And


options_schema = Schema(
    {'window': And(int, lambda x: 1 <= x)},
    ignore_extra_keys=True,
)
