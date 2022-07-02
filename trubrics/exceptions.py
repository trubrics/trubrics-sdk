class ValidationOutputError(BaseException):
    """An exception signalling that the output from a validation function is invalid."""


class PandasSchemaError(BaseException):
    """An exception signalling that two DataFrames do not have the same schema (column names & types)."""


class ClassifierNotSupportedError(BaseException):
    """An exception signalling that the output from a validation function is invalid."""
