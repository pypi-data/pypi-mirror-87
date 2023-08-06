from schema import Schema, And


options_schema = Schema(
    {'components': And(int, lambda x: 2 <= x)},
    ignore_extra_keys=True,
)
