import pytest

from trubrics.exceptions import EstimatorTypeError, SklearnMetricTypeError


def test__validate_minimum_functionality(validator_classifier):
    result = validator_classifier._validate_minimum_functionality()
    actual = True, {}
    assert result == actual


def test__validate_minimum_functionality_in_range_raises(validator_classifier):
    with pytest.raises(EstimatorTypeError):
        validator_classifier._validate_minimum_functionality_in_range()


@pytest.mark.parametrize(
    "kwargs,outcome,actual_result",
    [
        (
            {"metric": "accuracy", "threshold": 0.7, "dataset": "testing_data", "data_slice": None},
            False,
            {"performance": 0.5, "sample_size": 6},
        ),
        (
            {"metric": "accuracy", "threshold": 0.1, "dataset": "testing_data", "data_slice": None},
            True,
            {"performance": 0.5, "sample_size": 6},
        ),
        (
            {"metric": "my_custom_loss", "threshold": -0.7, "dataset": "testing_data", "data_slice": None},
            True,
            {"performance": -0.5, "sample_size": 6},
        ),
        (
            {"metric": "my_custom_loss", "threshold": -0.1, "dataset": "testing_data", "data_slice": None},
            False,
            {"performance": -0.5, "sample_size": 6},
        ),
        (
            {"metric": "accuracy", "threshold": 0.9, "dataset": "testing_data", "data_slice": "female"},
            False,
            {"performance": 0.0, "sample_size": 1},
        ),
    ],
)
def test__validate_performance_against_threshold(validator_classifier, kwargs, outcome, actual_result):
    result = validator_classifier._validate_performance_against_threshold(**kwargs)
    actual = outcome, actual_result
    assert result == actual


@pytest.mark.parametrize(
    "kwargs,error",
    [
        ({"metric": "accuracy", "threshold": "something", "dataset": "testing_data", "data_slice": None}, TypeError),
        (
            {"metric": "some_metric", "threshold": 10, "dataset": "testing_data", "data_slice": None},
            SklearnMetricTypeError,
        ),
        ({"metric": "accuracy", "threshold": 10, "dataset": "other_data", "data_slice": None}, ValueError),
        (
            {"metric": "accuracy", "threshold": 10, "dataset": "testing_data", "data_slice": "random_data_slice"},
            ValueError,
        ),
    ],
)
def test__validate_performance_against_threshold_raises(validator_classifier, kwargs, error):
    with pytest.raises(error):
        validator_classifier._validate_performance_against_threshold(**kwargs)


def test__validate_test_performance_against_dummy(validator_classifier):
    result = validator_classifier._validate_test_performance_against_dummy(metric="accuracy", strategy="most_frequent")
    result[1]["dummy_performance"] = round(result[1]["dummy_performance"], 2)

    actual = False, {"dummy_performance": 0.67, "test_performance": 0.5, "sample_size": 6}
    assert result == actual


def test__validate_performance_between_train_and_test(validator_classifier):
    result = validator_classifier._validate_performance_between_train_and_test(metric="accuracy", threshold=1)
    actual = False, {"train_performance": 1 / 3, "test_performance": 0.5, "train_sample_size": 6, "test_sample_size": 6}
    assert result == actual


def test__validate_inference_time(validator_classifier):
    result = validator_classifier._validate_inference_time(threshold=0.1, n_executions=10)
    result[1]["inference_time"] = round(result[1]["inference_time"], 1)

    actual = True, {"inference_time": 0}
    assert result == actual


def test__validate_feature_in_top_n_important_features(validator_classifier):
    result = validator_classifier._validate_feature_in_top_n_important_features(
        dataset="testing_data",
        feature="Age",
        top_n_features=2,
        permutation_kwargs={"n_repeats": 1, "random_state": 88, "n_jobs": -1},
    )
    result[1].pop("feature_importance")
    assert result == (True, {"feature_importance_ranking": 1})


def test__validate_feature_importance_between_train_and_test(validator_classifier):
    result = validator_classifier._validate_feature_importance_between_train_and_test(
        top_n_features=2, permutation_kwargs={"n_repeats": 1, "random_state": 88, "n_jobs": -1}
    )
    assert result[0] is False
