from sklearn.metrics import accuracy_score

from trubrics.context import ModelContext
from trubrics.validators.base import Validator


class RuleBasedModel:
    """
    This example shows how we can wrap python code into a model that can be used by the ModelContext.

    Tip: A custom model is built with python class that must contain:
        - an attribute named _estimator_type (see attributes bellow).
        - a predict() method with a pandas dataframe input argument,
          that returns a pandas series / numpy array of predict values
          (see source code bellow).

    Attributes:
        _estimator_type: the estimator type can either be 'classifier' or 'regressor'.

    Example:
        ```py
        from sklearn.metrics import accuracy_score
        estimator = RuleBasedModel()
        model_context = ModelContext(estimator=estimator, evaluation_function=accuracy_score)
        ```
    """

    def __init__(self):
        self._estimator_type = "classifier"

    def predict(self, df):
        """Rule based predict classification function to determine a class based on single feature."""
        df["Survived"] = df["Age"].apply(lambda x: 0 if x > 40 else 1)
        return df["Survived"]


def custom_model_context():
    estimator = RuleBasedModel()
    model_context = ModelContext(estimator=estimator, evaluation_function=accuracy_score)
    return model_context


def test_performance_validation(data_context):
    model_validator = Validator(data=data_context, model=custom_model_context())

    result = model_validator._validate_performance_against_threshold(threshold=0.7)
    actual = False, {"performance": 1 / 3}
    assert result == actual


def test_biased_performance_validation(data_context):
    model_validator = Validator(data=data_context, model=custom_model_context())
    result = model_validator._validate_biased_performance_across_category("Sex", 0.5)
    actual = True, {"max_performance_difference": 0.4}
    assert result == actual
