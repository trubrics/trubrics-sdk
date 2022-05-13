from typing import Callable

import pandas as pd

from trubrics.base import BaseModel, BaseTester


def test_performance_against_threshold(
    model: Callable,
    test_data: pd.DataFrame,
    evaluation_function: Callable,
    target: str,
    runner: str,
    threshold: float = 0.8,
):
    """
    Compares performance of a model on a dataset to a hard coded threshold value.
    """
    model = BaseModel(model)

    if evaluation_function.__name__ == "accuracy_score":
        type = "greater"
    else:
        NotImplementedError("The evaluation type is not recognized.")
    predictions = model.predict(test_data)
    result = evaluation_function(test_data[target], predictions)
    BaseTester(result, threshold).assertion(type=type, runner=runner)
