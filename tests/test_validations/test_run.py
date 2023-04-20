import pytest

from examples.classification_titanic.custom_scorer import custom_scorers
from examples.classification_titanic.custom_validator import CustomValidator
from trubrics.exceptions import UnknownValidationError
from trubrics.validations import Trubric
from trubrics.validations.run import TrubricRun


def test_run_trubric(data_context, classifier_model, trubric):
    run_context = TrubricRun(
        data_context=data_context,
        model=classifier_model,
        custom_validator=CustomValidator,
        trubric=trubric,
        custom_scorers=custom_scorers,
    )
    all_validation_results = run_context.generate_validations_from_trubric()

    actuals = (
        ("validate_minimum_functionality", "error", True),
        ("validate_performance_against_threshold", "experiment", True),
        ("validate_master_age", "warning", True),
    )

    for actual, result in zip(actuals, all_validation_results):
        assert result.validation_type == actual[0]
        assert result.severity == actual[1]
        assert result.passed == actual[2]


def test_run_trubric_raises(data_context, classifier_model):
    trubric_dict = {
        "name": "my_first_trubric",
        "passed": False,
        "total_passed": 0,
        "total_failed": 1,
        "failing_severity": "warning",
        "model_name": "my_model",
        "model_version": 0.1,
        "data_context_name": "my_first_dataset",
        "data_context_version": 0.1,
        "metadata": {"tag": "master"},
        "validations": [
            {
                "validation_type": "some_random_validation_name_that_is_not_in_a_validator",
                "validation_kwargs": {"args": [], "kwargs": {}},
                "explanation": "some docstring",
                "passed": False,
                "severity": "warning",
                "result": {},
            }
        ],
    }
    trubric = Trubric.parse_obj(trubric_dict)
    run_context = TrubricRun(
        data_context=data_context,
        model=classifier_model,
        trubric=trubric,
        custom_scorers=custom_scorers,
    )
    all_validation_results = run_context.generate_validations_from_trubric()

    with pytest.raises(UnknownValidationError):
        for validation in all_validation_results:
            pass
