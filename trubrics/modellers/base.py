from abc import ABC, abstractmethod


class BaseModeller(ABC):
    @abstractmethod
    def predict(self):
        """Use the estimator to predict on the test data."""

    @abstractmethod
    def explore_test_set_errors(self):
        """Filter the testing data on errors."""

    @abstractmethod
    def compute_performance_on_test_set(self):
        """Calculate the performance on the test set with the evaluation function."""
