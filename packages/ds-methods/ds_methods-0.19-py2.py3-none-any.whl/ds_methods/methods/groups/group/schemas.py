from schema import Schema, And, Optional


# grouping parameters
# keys - by which columns
# time - hours
options_schema = Schema(
    And({
        Optional('keys'): And([str], len),
        Optional('time'): And(int, lambda x: 1 <= x <= 24),
    }, lambda x: 'keys' in x or 'time' in x),
    ignore_extra_keys=True,
)
