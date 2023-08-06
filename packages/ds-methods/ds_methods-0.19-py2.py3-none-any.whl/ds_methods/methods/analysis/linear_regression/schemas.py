from schema import Schema


options_schema = Schema(
    {
        'columns': [str, str],
    },
    ignore_extra_keys=True,
)
