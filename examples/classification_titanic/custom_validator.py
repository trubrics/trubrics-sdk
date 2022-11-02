from trubrics.context import DataContext
from trubrics.validations import ModelValidator
from trubrics.validations.validation_output import (
    validation_output,
    validation_output_type,
)


class CustomValidator(ModelValidator):
    def __init__(self, data: DataContext, model, custom_scorers=None, slicing_functions=None):
        super().__init__(data, model, custom_scorers, slicing_functions)

    def _validate_master_age(self, age_limit_master) -> validation_output_type:
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
        master_df = self.tm.data.testing_data.loc[lambda df: df["Title"] == "Master"]
        errors_df = master_df.loc[lambda df: df["Age"] >= age_limit_master]
        return len(errors_df) == 0, {"errors_df": errors_df.to_dict()}

    @validation_output
    def validate_master_age(self, age_limit_master: int, severity=None):
        """Validate that passengers with the title "master" are younger than a certain age

        Args:
            age_limit_master: cut off value for master

        Returns:
            True for success, false otherwise. With a results dictionary giving dict of errors.
        """
        return self._validate_master_age(age_limit_master)
