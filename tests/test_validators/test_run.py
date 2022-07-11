from trubrics.validators.run import run_trubric


def test_run_trubric(data_context, classifier_model_context, validator_classifier, trubric):
    all_validation_results = run_trubric(
        data_context=data_context,
        model_context=classifier_model_context,
        custom_validator=validator_classifier,
        trubric_path=trubric[0],  # trubric_filename
    )

    actuals = (
        ("validate_single_edge_case", "warning", "fail"),
        ("validate_feature_in_top_n_important_features", "error", "pass"),
        ("validate_performance_for_different_fares", "warning", "pass"),
    )

    for actual, result in zip(actuals, all_validation_results):
        assert result == actual
