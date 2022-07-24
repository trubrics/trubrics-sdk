# The `Validator` object

The trubrics library comes with ready-to-use validations that you can test against your models in a
couple of lines of code. To instantiate the `Validator` (that holds all validations) with your DataContext
and ModelContext, run:

--8<-- "docs/snippets/create_validations.md"

The `Validator` object respects the following conventions:

- Contains all code for validations
- Validations are built with two methods:
    - A method with an underscored prefix e.g. "_validate_something". This method contains all code logic for the validation,
    and must have an output of a boolean variable that indicates a pass / fail of the validation, and a dictionary that holds
    contextual information that is calculated during the validation run. This method is unit tested and documented.
    - The second method has the same name, without the underscore prefix e.g. "validate_something". This method is used to call
    the validation, and formats the output with the [the `validation_output` decorator](##the-validation_output-decorator).
- All validation methods must

## The `validation_output` decorator
The validation output decorator transforms the output of a validation function into a `ValidationContext`.
