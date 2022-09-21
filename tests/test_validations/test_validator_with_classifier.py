import pytest

from trubrics.exceptions import EstimatorTypeError


def test__validate_minimum_functionality(validator_classifier):
    result = validator_classifier._validate_minimum_functionality()
    actual = True, {}
    assert result == actual


def test__validate_minimum_functionality_in_range_raises(validator_classifier):
    with pytest.raises(EstimatorTypeError):
        validator_classifier._validate_minimum_functionality_in_range()


def test__validate_performance_against_threshold(validator_classifier):
    result = validator_classifier._validate_performance_against_threshold(metric="accuracy", threshold=0.7)
    actual = False, {"performance": 0.5}
    assert result == actual


def test__validate_biased_performance_across_category(validator_classifier):
    result = validator_classifier._validate_biased_performance_across_category(
        metric="accuracy", category="Sex", threshold=0.2
    )
    actual = False, {"max_performance_difference": 0.6}
    assert result == actual


def test__validate_performance_against_dummy(validator_classifier):
    result = validator_classifier._validate_performance_against_dummy(metric="accuracy", strategy="most_frequent")
    result[1]["dummy_performance"] = round(result[1]["dummy_performance"], 2)

    actual = False, {"dummy_performance": 0.67, "test_performance": 0.5}
    assert result == actual


def test__validate_performance_between_train_and_test(validator_classifier):
    result = validator_classifier._validate_performance_between_train_and_test(metric="accuracy", threshold=1)
    actual = False, {"train_score": 1 / 3, "test_score": 0.5}
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
