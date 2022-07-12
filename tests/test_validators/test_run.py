import pytest

from trubrics.context import TrubricContext
from trubrics.exceptions import UnknownValidationError
from trubrics.validators.run import run_trubric


def test_run_trubric(data_context, classifier_model_context, custom_validator_classifier, trubric):
    all_validation_results = run_trubric(
        data_context=data_context,
        model_context=classifier_model_context,
        custom_validator=custom_validator_classifier,
        trubric=trubric,
    )

    actuals = (
        ("validate_single_edge_case", "warning", "fail"),
        ("validate_feature_in_top_n_important_features", "error", "pass"),
        ("validate_performance_for_different_fares", "warning", "fail"),
    )

    for actual, result in zip(actuals, all_validation_results):
        assert result == actual


def test_run_trubric_raises(data_context, classifier_model_context):
    trubric_dict = {
        "name": "",
        "model_context_name": "",
        "model_context_version": 0,
        "data_context_name": "",
        "data_context_version": 0,
        "metadata": None,
        "validations": [
            {
                "validation_type": "some_random_validation_name_that_is_not_in_a_validator",
                "validation_kwargs": {"args": [], "kwargs": {}},
                "outcome": "fail",
                "severity": "warning",
                "result": {},
            }
        ],
    }
    trubric = TrubricContext.parse_obj(trubric_dict)
    all_validation_results = run_trubric(
        data_context=data_context, model_context=classifier_model_context, custom_validator=None, trubric=trubric
    )

    with pytest.raises(UnknownValidationError):
        for validation in all_validation_results:
            pass
