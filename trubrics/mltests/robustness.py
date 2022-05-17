from typing import Type, Union

import pandas as pd

from trubrics.base import BaseModel, BaseTester


def test_single_edge_case(
    model: Type,
    data: pd.DataFrame,
    desired_output: Union[int, float],
    runner: str,
):
    """
    Single edge case test that:
        - reads the test config about the schema & data (features and expected output)
        - calls .predict() on the model with the stored data
        - tests the output of that model versus the desired output
    """
    trubrics_model = BaseModel(model)
    model_prediction = trubrics_model.predict(data)
    BaseTester(model_prediction, desired_output).assertion(type="equals", runner=runner)
