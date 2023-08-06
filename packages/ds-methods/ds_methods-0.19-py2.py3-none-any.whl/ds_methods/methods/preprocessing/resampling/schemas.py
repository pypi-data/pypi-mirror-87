from schema import Schema, And


options_schema = Schema(
    {
        'rule': And(str, len),
    },
    ignore_extra_keys=True,
)
