from typing import Callable, Union

import numpy as np

from mlting.utils.loader import baseTester
from mlting.utils.model import baseModel


def single_edge_case(
    model: Callable,
    data: np.array,
    desired_output: Union[int, str],
    runner: str,
):
    """
    Single edge case test that:
        - reads the test config about the schema & data (features and expected output)
        - calls .predict() on the model with the stored data
        - tests the output of that model versus the desired output
    """
    model = baseModel(model)
    model_prediction = model.predict(data)
    baseTester().assert_equals(model_prediction, desired_output, runner)
