from schema import Schema, And, Optional


options_schema = Schema(
    And({
        Optional('include'): [str],
        Optional('exclude'): [str],
    }, lambda x: 'include' in x or 'exclude' in x),
    ignore_extra_keys=True,
)
