from schema import Schema, And


options_schema = Schema(
    {'clusters': And(int, lambda x: 2 <= x)},
    ignore_extra_keys=True,
)
