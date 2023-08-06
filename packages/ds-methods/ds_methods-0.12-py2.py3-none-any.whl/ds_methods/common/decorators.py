import traceback
from typing import Callable
from functools import wraps

from ds_methods.common.types import MethodOutput


def catch_method_error():
    def wrapped_catch_method_error(f: Callable):
        @wraps(f)
        def decorated_function(input_data, *args, **kwargs) -> MethodOutput:
            try:
                return f(input_data, *args, **kwargs)
            except Exception:
                traceback.print_exc()
                return MethodOutput(error=traceback.format_exc())

        return decorated_function

    return wrapped_catch_method_error
