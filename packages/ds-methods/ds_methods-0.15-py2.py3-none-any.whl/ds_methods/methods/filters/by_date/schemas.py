from datetime import datetime
from dateutil.parser import parse
from schema import Schema, Optional, And, Use, Or


options_schema = Schema(
    And({
        Optional('gte'): And(Or(datetime, str), Use(lambda x: parse(x) if isinstance(x, str) else x)),
        Optional('lte'): And(Or(datetime, str), Use(lambda x: parse(x) if isinstance(x, str) else x)),
    }, lambda x: 'gte' in x or 'lte' in x),
    ignore_extra_keys=True,
)
