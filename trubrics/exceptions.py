class ValidationOutputError(Exception):
    """An exception signalling that the output from a validation function is invalid."""


class PandasSchemaError(Exception):
    """An exception signalling that two DataFrames do not have the same schema (column names & types)."""


class UnknownValidationError(Exception):
    """An exception signalling that validation is not recognised by a given validator."""


class MissingConfigPathError(Exception):
    """An exception signalling that the trubrics config file path does not exist."""


class MissingTrubricRunFileError(Exception):
    """An exception signalling that a TrubricRun file does not exist."""


class EstimatorTypeError(Exception):
    """An exception signalling that the estimator is not of type 'classifier' or 'regressor'."""


class SklearnMetricTypeError(Exception):
    """An exception signalling that the metric provided does not refer to an sklearn default metric."""


class ModelPredictionError(Exception):
    """An exception signalling that the model can't predict on a given set."""


class EmptyDfError(Exception):
    """An exception signalling that the dataframe is empty."""
