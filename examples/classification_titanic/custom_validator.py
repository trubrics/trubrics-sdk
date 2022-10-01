from trubrics.context import DataContext
from trubrics.validations import ModelValidator
from trubrics.validations.validation_output import (
    validation_output,
    validation_output_type,
)


class CustomValidator(ModelValidator):
    def __init__(self, data: DataContext, model, custom_scorers=None, slicing_functions=None):
        super().__init__(data, model, custom_scorers, slicing_functions)

    @validation_output
    def validate_performance_for_different_fares(self, fare_cutoff: int, severity=None):
        """Validate the models performance for expensive vs cheap tickets.

        Args:
            fare_cutoff: value to split the fare column on

        Returns:
            True for success, false otherwise. With a results dictionary giving all the number of errors by fare split.
        """
        return self._validate_performance_for_different_fares(fare_cutoff)

    def _validate_performance_for_different_fares(self, fare_cutoff: int = 50) -> validation_output_type:
        """
        Write your custom validation function here.

        Notes
        -----
            This method is separated from validate_performance_for_different_fares
            to apply @validation_output and for unit testing.

            The @validation_output decorator allows you to generate a Validation object,
            and must be used to be able to save your validation as part of a Trubric.
            This decorator requires you to return values with the same type as validation_output_type.
        """

        errors_df = self.tm.testing_data_errors
        number_of_errors_by_fare_ratio = (
            errors_df.loc[lambda x: x["Fare"] <= fare_cutoff].shape[0]
            / errors_df.loc[lambda x: x["Fare"] > fare_cutoff].shape[0]
        )
        return (
            number_of_errors_by_fare_ratio > 0.5 and number_of_errors_by_fare_ratio < 1.5,
            {"number_of_errors_by_fare_ratio": round(number_of_errors_by_fare_ratio, 3)},
        )
