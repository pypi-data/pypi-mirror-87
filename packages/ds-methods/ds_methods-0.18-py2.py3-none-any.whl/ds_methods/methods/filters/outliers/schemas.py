from schema import Schema, Optional, And, Or

from ds_methods.common.enums import BaseEnum


class OutliersHows(BaseEnum):
    All = 'all'
    Any = 'any'


class OutliersMethods(BaseEnum):
    Get = 'get'
    Remove = 'remove'


options_schema = Schema(
    {
        Optional('include', default=None): [str],
        Optional('exclude', default=None): [str],
        Optional('threshold', default=3): And(Or(int, float), lambda x: x >= 0),
        Optional('how', default=OutliersHows.All): And(str, lambda x: OutliersHows.validate(x)),
        Optional('method', default=OutliersMethods.Remove): And(str, lambda x: OutliersMethods.validate(x)),
    },
    ignore_extra_keys=True,
)
