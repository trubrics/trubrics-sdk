import json
from typing import Any, Callable

from trubrics.context import ValidationContext


def validation_output(func: Callable) -> Callable:
    """Decorative function for validation point outputs."""

    def inner(*args, **kwargs) -> ValidationContext:
        outcome, result = func(*args, **kwargs)
        outcome = _pass_or_fail(outcome)
        jsonable_args = [arg for arg in args if _is_jsonable(arg)]
        jsonable_kwargs = {key: val for key, val in kwargs.items() if _is_jsonable(val)}
        _is_jsonable(result, raise_error=True)

        return ValidationContext(
            validation_type=func.__name__,
            validation_kwargs={"args": jsonable_args, "kwargs": jsonable_kwargs},
            outcome=outcome,
            result=result,
        )

    return inner


def _is_jsonable(x: Any, raise_error: bool = False) -> bool:
    try:
        json.dumps(x)
        return True
    except (OverflowError, TypeError) as e:
        if raise_error:
            raise e
        return False


def _pass_or_fail(condition: bool) -> str:
    return "pass" if condition else "fail"
