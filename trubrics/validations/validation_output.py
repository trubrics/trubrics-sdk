import json
from functools import wraps
from typing import Any, Callable, Dict, Tuple, Union

import numpy as np
from typeguard import check_type

from trubrics.context import TrubricsModel
from trubrics.exceptions import ValidationOutputError
from trubrics.validations.dataclass import Validation

validation_output_type = Tuple[Union[bool, np.bool_], Dict[str, Union[dict, str, int, float, np.generic]]]


def validation_output(func: Callable) -> Callable:
    """Decorative function for validation point outputs."""

    @wraps(func)
    def inner(*args, **kwargs) -> Validation:
        output = func(*args, **kwargs)

        try:
            check_type("output", output, validation_output_type)
        except TypeError:
            raise ValidationOutputError(
                f"Each validation should return an outcome and a result with type: {validation_output_type}"
            )

        outcome, result = output
        outcome = _pass_or_fail(outcome)

        if kwargs.get("severity"):
            severity = kwargs.pop("severity")
        else:
            severity = "error"

        if len(args) > 1:
            args = args[1:]  # ignore self arg for class methods
        else:
            args = ()

        typed_args = _correct_types_for_json(args)
        typed_kwargs = _correct_types_for_json(kwargs)
        typed_result = _correct_types_for_json(result)

        _is_jsonable(typed_args, raise_error=True)
        _is_jsonable(typed_kwargs, raise_error=True)
        _is_jsonable(typed_result, raise_error=True)

        if func.__doc__ is None:
            raise TypeError(
                "Validations require a docstring to explain the validation's purpose and required parameters."
            )
        stripped_docstring = "\n".join(" ".join(line.split()) for line in func.__doc__.split("\n"))

        return Validation(
            validation_type=func.__name__,
            validation_kwargs={"args": typed_args, "kwargs": typed_kwargs},
            explanation=stripped_docstring,
            outcome=outcome,
            severity=severity,
            result=typed_result,  # type: ignore
        )

    return inner


def _correct_types_for_json(value: Any):
    if isinstance(value, dict):
        return {_correct_types_for_json(key): _correct_types_for_json(val) for key, val in value.items()}
    elif isinstance(value, list):
        return [_correct_types_for_json(arg) for arg in value]
    elif isinstance(value, np.generic):
        return value.item()
    elif value != value:
        return None  # replace NaN with None for json serialisation
    else:
        return value


def _is_jsonable(obj: Any, raise_error: bool = False) -> bool:
    try:
        json.dumps(obj)
        return True
    except (OverflowError, TypeError) as e:
        if isinstance(obj, TrubricsModel):
            return False
        elif raise_error:
            raise e
        else:
            return False


def _pass_or_fail(condition: bool) -> str:
    return "pass" if condition else "fail"
