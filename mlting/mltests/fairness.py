import numpy as np
from sklearn.metrics import accuracy_score
from trubrics.base import BaseModel, BaseTester
from trubrics.utils.pandas import get_features


def test_biased_performance_across_category(
    model, test_data, category, target, runner, evaluation_function=accuracy_score, threshold=0.1
):
    """
    Calculates various performance over values in a category and tests for
    a difference in performance inferior to the threshold value.

    TODO:
    - More complex threshold function
    - Modify cardinality

    To add to output report:
    - Show distributions of category variables
    - Performance plots of results
    """
    model = BaseModel(model)
    cat_values = test_data[category].unique()
    if len(cat_values) > 20:
        raise Exception(f"Cardinality of {len(cat_values)} too high for performance test.")
    if category not in test_data.columns:
        raise KeyError(f"Column '{category}' not found in dataset.")
    result = {}
    for value in cat_values:
        if value not in [np.nan, None]:
            filtered_data = test_data.query(f"`{category}`=='{value}'")
            predictions = model.predict(filtered_data.loc[:, get_features(filtered_data, target)])
            result[value] = evaluation_function(filtered_data[target], predictions)
    max_performance_difference = max(result.values()) - min(result.values())
    BaseTester(max_performance_difference, threshold).assertion(type="less", runner=runner)
    # return result


def test_biased_positive_outcome():
    """
    is the positive (survived in titanic UC) outcome of the
    model more likely to happen to a specific group in a single column?
    """
    return None
