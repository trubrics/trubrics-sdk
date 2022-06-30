import json
from typing import Any, Callable, Dict, Tuple, Union

from typeguard import check_type

from trubrics.context import ValidationContext
from trubrics.exceptions import ValidationOutputError
from trubrics.modellers.classifier import Classifier

validation_output_type = Tuple[bool, Dict[str, Union[str, int, float]]]


def validation_output(func: Callable) -> Callable:
    """Decorative function for validation point outputs."""

    def inner(*args, **kwargs) -> ValidationContext:
        output = func(*args, **kwargs)

        try:
            check_type("output", output, validation_output_type)
        except TypeError:
            raise ValidationOutputError(
                f"Each validation should return an outcome and a result with type: {validation_output_type}"
            )

        outcome, result = output

        outcome = _pass_or_fail(outcome)

        if len(args) > 1:
            args = args[1:]  # ignore self arg for class methods
        else:
            args = ()

        jsonable_args = [arg for arg in args if _is_jsonable(arg, raise_error=True)]
        jsonable_kwargs = {key: val for key, val in kwargs.items() if _is_jsonable(val, raise_error=True)}
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
        if isinstance(x, Classifier):
            return False
        elif raise_error:
            raise e
        else:
            return False


def _pass_or_fail(condition: bool) -> str:
    return "pass" if condition else "fail"
