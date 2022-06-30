from trubrics.modellers.base import Modeller


class Regressor(Modeller):
    """Classifier class with methods combining data and model contexts."""

    def explore_test_set_errors(self):
        """Filter the testing data on errors."""
        raise NotImplementedError()
