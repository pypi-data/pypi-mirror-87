from schema import Schema, And

# 'days' should non empty list of integers and each element should be more then 1
options_schema = Schema(
    {'days': And([int], len, lambda x: 1 <= min(x))},
    ignore_extra_keys=True,
)
