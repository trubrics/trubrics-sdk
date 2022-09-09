class ValidationOutputError(Exception):
    """An exception signalling that the output from a validation function is invalid."""


class PandasSchemaError(Exception):
    """An exception signalling that two DataFrames do not have the same schema (column names & types)."""


class ClassifierNotSupportedError(Exception):
    """An exception signalling that the output from a validation function is invalid."""


class UnknownValidationError(Exception):
    """An exception signalling that validation is not recognised by a given validator."""


class MissingConfigPathError(Exception):
    """..."""


class MissingTrubricRunFileError(Exception):
    """..."""


class EstimatorTypeError(Exception):
    """Estimator is not of type 'classifier' or 'regressor'."""


class SklearnMetricTypeError(Exception):
    """."""


class ModelPredictionError(Exception):
    """Model doesn't predict on a dataset."""
