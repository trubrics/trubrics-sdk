from sklearn.metrics import accuracy_score

from mlting.utils.pandas import get_features


def test_biased_performance_across_category(
    model, test_data, category, target, evaluation_function=accuracy_score, threshold=0.1
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
    categories = test_data[category].unique()
    if len(categories) > 20:
        raise Exception("Cardinality too high for performance test.")
    result = {}
    for value in categories:
        filtered_data = test_data.query(f"`{category}`=='{value}'")
        predictions = model.predict(filtered_data.loc[:, get_features(filtered_data, target)])
        result[value] = evaluation_function(filtered_data[target], predictions)
    if max(result.values()) - min(result.values()) > threshold:
        print("Test failed.")
    else:
        print("Test passed.")
    return result
