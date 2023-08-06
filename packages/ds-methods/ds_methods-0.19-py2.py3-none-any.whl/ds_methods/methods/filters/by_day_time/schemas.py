from datetime import time
from schema import Schema


options_schema = Schema(
    {'gte': time, 'lte': time},
    ignore_extra_keys=True,
)
