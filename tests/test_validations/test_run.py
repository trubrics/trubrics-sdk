import pytest

from examples.cli.custom_scorer import custom_scorers
from examples.cli.custom_validator import CustomValidator
from trubrics.context import TrubricContext
from trubrics.exceptions import UnknownValidationError
from trubrics.validations.run import run_trubric


def test_run_trubric(data_context, classifier_model, trubric):
    all_validation_results = run_trubric(
        data_context=data_context,
        model=classifier_model,
        custom_validator=CustomValidator,
        trubric=trubric,
        custom_scorers=custom_scorers,
    )

    actuals = (
        ("validate_single_edge_case", "warning", "fail"),
        ("validate_performance_against_threshold", "experiment", "pass"),
        ("validate_feature_in_top_n_important_features", "error", "pass"),
        ("validate_performance_for_different_fares", "warning", "fail"),
    )

    for actual, result in zip(actuals, all_validation_results):
        assert result.validation_type == actual[0]
        assert result.severity == actual[1]
        assert result.outcome == actual[2]


def test_run_trubric_raises(data_context, classifier_model):
    trubric_dict = {
        "trubric_name": "my_first_trubric",
        "metric": "accuracy",
        "model_name": "my_model",
        "model_version": 0.1,
        "data_context_name": "my_first_dataset",
        "data_context_version": 0.1,
        "metadata": {"tag": "master"},
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
        data_context=data_context, model=classifier_model, custom_validator=None, trubric=trubric
    )

    with pytest.raises(UnknownValidationError):
        for validation in all_validation_results:
            pass
