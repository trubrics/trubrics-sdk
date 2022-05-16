from typing import Type, Union

import pandas as pd


class BaseModel:
    """Base class for Models."""

    def __init__(self, model: Type):
        self.model = model

    def predict(self, data: pd.DataFrame):
        try:
            return self.model.predict(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def predict_proba(self, data: pd.DataFrame):
        try:
            return self.model.predict_proba(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error


class BaseTester:
    """Base class for tests."""

    def __init__(self, actual: Union[str, int], desired: Union[str, int]):
        self.actual_outcome = actual
        self.desired_outcome = desired

    def assertion(self, type: str = "equals", runner: str = "notebook"):
        assertion_function = getattr(self, f"_{type}")
        if runner == "notebook":
            if assertion_function():
                print("Test passed.")
            else:
                print("Test failed.")
        elif runner == "unit":
            assert assertion_function()
        else:
            raise NotImplementedError(f"{runner} is not a valid Runner.")

    def _equals(self):
        return self.actual_outcome == self.desired_outcome

    def _greater(self):
        self._check_numerical()
        return self.actual_outcome > self.desired_outcome

    def _greater_equal(self):
        self._check_numerical()
        return self.actual_outcome >= self.desired_outcome

    def _less(self):
        self._check_numerical()
        return self.actual_outcome < self.desired_outcome

    def _less_equal(self):
        self._check_numerical()
        return self.actual_outcome <= self.desired_outcome

    def _check_numerical(self):
        if not isinstance(self.actual_outcome, (int, float)) or not isinstance(self.desired_outcome, (int, float)):
            raise TypeError("Values must both be of numerical (int or float) type.")
