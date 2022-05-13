from typing import Callable


class BaseModel:
    """Base class for Models."""

    def __init__(self, model: Callable):
        self.model = model

    def predict(self, data):
        try:
            return self.model.predict(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def predict_proba(self, data):
        try:
            return self.model.predict_proba(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error


class BaseTester:
    """Base class for tests."""

    def __init__(self, actual, desired):
        self.actual_outcome = actual
        self.desired_outcome = desired

    def assertion(self, type="equals", runner="notebook"):
        assertion_function = getattr(self, type)
        if runner == "notebook":
            if assertion_function():
                print("Test passed.")
            else:
                print("Test failed.")
        elif runner == "unit":
            assert assertion_function()
        else:
            raise NotImplementedError(f"{runner} is not a valid Runner.")

    def equals(self):
        return self.actual_outcome == self.desired_outcome

    def greater(self):
        return self.actual_outcome > self.desired_outcome

    def greater_equal(self):
        return self.actual_outcome >= self.desired_outcome

    def less(self):
        return self.actual_outcome < self.desired_outcome

    def less_equal(self):
        return self.actual_outcome <= self.desired_outcome
