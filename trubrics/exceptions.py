class ValidationOutputError(Exception):
    """An exception signalling that the output from a validation function is invalid."""


class PandasSchemaError(Exception):
    """An exception signalling that two DataFrames do not have the same schema (column names & types)."""


class ClassifierNotSupportedError(Exception):
    """An exception signalling that the output from a validation function is invalid."""


class UnknownEstimatorType(Exception):
    """An exception signalling that an estimator type is not recognised."""


class UnknownValidationError(Exception):
    """An exception signalling that validation is not recognised by a given validator."""
