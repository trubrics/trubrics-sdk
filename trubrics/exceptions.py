class ValidationOutputError(BaseException):
    """An exception signalling that the output from a validation function is invalid."""


class PandasSchemaError(BaseException):
    """An exception signalling that two DataFrames do not have the same schema (column names & types)."""


class ClassifierNotSupportedError(BaseException):
    """An exception signalling that the output from a validation function is invalid."""


class UnknownEstimatorType(BaseException):
    """An exception signalling that an estimator type is not recognised."""


class UnknownValidationError(BaseException):
    """An exception signalling that validation is not recognised by a given validator."""
