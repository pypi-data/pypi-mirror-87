from schema import Schema, And, Or


options_schema = Schema(
    {
        'prefixes': And([str], len),
        'axis': Or(0, 1),
    },
    ignore_extra_keys=True,
)
