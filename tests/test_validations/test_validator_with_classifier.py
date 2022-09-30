import pandas as pd
import pytest

from trubrics.exceptions import EmptyDfError, EstimatorTypeError, SklearnMetricTypeError


def test__validate_minimum_functionality(validator_classifier):
    actual = validator_classifier._validate_minimum_functionality()
    expected = True, {}
    assert actual == expected


def test__validate_minimum_functionality_in_range_raises(validator_classifier):
    with pytest.raises(EstimatorTypeError):
        validator_classifier._validate_minimum_functionality_in_range()


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {"metric": "accuracy", "threshold": 0.7, "dataset": "testing_data", "data_slice": None},
            (False, {"performance": 0.5, "sample_size": 6}),
        ),
        (
            {"metric": "accuracy", "threshold": 0.1, "dataset": "testing_data", "data_slice": None},
            (True, {"performance": 0.5, "sample_size": 6}),
        ),
        (
            {"metric": "my_custom_loss", "threshold": -0.7, "dataset": "testing_data", "data_slice": None},
            (True, {"performance": -0.5, "sample_size": 6}),
        ),
        (
            {"metric": "my_custom_loss", "threshold": -0.1, "dataset": "testing_data", "data_slice": None},
            (False, {"performance": -0.5, "sample_size": 6}),
        ),
        (
            {"metric": "accuracy", "threshold": 0.9, "dataset": "testing_data", "data_slice": "female"},
            (False, {"performance": 0.0, "sample_size": 1}),
        ),
    ],
)
def test__validate_performance_against_threshold(validator_classifier, kwargs, expected):
    actual = validator_classifier._validate_performance_against_threshold(**kwargs)
    assert actual == expected


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


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {"metric": "accuracy", "strategy": "most_frequent", "dummy_kwargs": None, "data_slice": None},
            (False, {"dummy_performance": 0.67, "test_performance": 0.5, "sample_size": 6}),
        ),
        (
            {"metric": "accuracy", "strategy": "constant", "dummy_kwargs": {"constant": 1}, "data_slice": None},
            (True, {"dummy_performance": 0.33, "test_performance": 0.5, "sample_size": 6}),
        ),
        (
            {"metric": "accuracy", "strategy": "most_frequent", "dummy_kwargs": None, "data_slice": "male"},
            (False, {"dummy_performance": 0.6, "test_performance": 0.6, "sample_size": 5}),
        ),
    ],
)
def test__validate_test_performance_against_dummy(validator_classifier, kwargs, expected):
    actual = validator_classifier._validate_test_performance_against_dummy(**kwargs)
    actual[1]["dummy_performance"] = round(actual[1]["dummy_performance"], 2)

    assert actual == expected


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        (
            {"metric": "accuracy", "threshold": 0.2, "data_slice": None},
            (
                False,
                {"train_performance": 1 / 3, "test_performance": 0.5, "train_sample_size": 6, "test_sample_size": 6},
            ),
        ),
    ],
)
def test__validate_performance_between_train_and_test(validator_classifier, kwargs, expected):
    actual = validator_classifier._validate_performance_between_train_and_test(**kwargs)
    assert actual == expected


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


def test__scorer_raises(validator_classifier):
    with pytest.raises(SklearnMetricTypeError):
        validator_classifier._scorer(metric="some_random_metric")


@pytest.mark.parametrize(
    "dataset,data_slice,error",
    [
        ("testing_data", "test_slice_function", TypeError),
        ("training_data", "children", EmptyDfError),
        ("training_data", "undefined_data_slice", ValueError),
    ],
)
def test__slice_data_with_slicing_function_raises(validator_classifier, dataset, data_slice, error):
    with pytest.raises(error):
        validator_classifier._slice_data_with_slicing_function(dataset=dataset, data_slice=data_slice)


def test__slice_data_with_slicing_function(validator_classifier):
    expected_X = pd.DataFrame(
        {
            "Sex": ["female"],
            "Embarked": ["C"],
            "Title": ["Miss"],
            "Pclass": [3],
            "Age": [9.0],
            "SibSp": [1],
            "Parch": [1],
            "Fare": [15.25],
        },
        index=[2],
    )
    expected_y = pd.Series(0, index=[2], name="Survived")

    actual = validator_classifier._slice_data_with_slicing_function(dataset="training_data", data_slice="female")
    pd.testing.assert_frame_equal(actual[0], expected_X)
    pd.testing.assert_series_equal(actual[1], expected_y)


def test__score_data_context_raises(validator_classifier):
    with pytest.raises(ValueError):
        validator_classifier._score_data_context(metric="accuracy", dataset="something", data_slice=None)
