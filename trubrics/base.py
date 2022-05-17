from typing import Type, Union

import numpy as np
import pandas as pd


class BaseModel:
    """Base class for Models."""

    def __init__(self, model: Type):
        self.model = model

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        try:
            return self.model.predict(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def predict_proba(self, data: pd.DataFrame) -> np.ndarray:
        try:
            return self.model.predict_proba(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error


class BaseTester:
    """Base class for tests."""

    def __init__(self, actual: Union[int, float], desired: Union[int, float]):
        if not isinstance(actual, (int, float)) or not isinstance(desired, (int, float)):
            raise TypeError("'actual' and 'desired' values should be numerical for comparison.")
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

    def _equals(self) -> bool:
        return self.actual_outcome == self.desired_outcome

    def _greater(self) -> bool:
        return self.actual_outcome > self.desired_outcome

    def _greater_equal(self) -> bool:
        return self.actual_outcome >= self.desired_outcome

    def _less(self) -> bool:
        return self.actual_outcome < self.desired_outcome

    def _less_equal(self) -> bool:
        return self.actual_outcome <= self.desired_outcome
