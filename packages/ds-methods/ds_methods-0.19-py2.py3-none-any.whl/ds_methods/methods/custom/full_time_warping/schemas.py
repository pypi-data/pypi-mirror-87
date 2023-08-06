from schema import Schema


options_schema = Schema(
    {'pair_column_prefix': str},
    ignore_extra_keys=True,
)
