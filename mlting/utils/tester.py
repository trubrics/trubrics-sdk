class BaseTester:
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

    def less(self):
        return self.actual_outcome < self.desired_outcome
