# The `ModelValidator` object

The trubrics library comes with ready-to-use validations that you can test against your models in a
couple of lines of code. These validations are held in the `ModelValidator` object, that can be instantiated
with your DataContext and a model:

--8<-- "docs/snippets/create_validations.md"

The `ModelValidator` object respects the following conventions:

- Contains all code for validations
- All validation names start with the prefix "validate_"
- Validations are built with two methods:
    - A method with an underscored prefix e.g. "_validate_something". This method contains all code logic for the validation,
    and must return a boolean variable that indicates a pass / fail of the validation, and a dictionary that holds
    contextual information that is calculated during the validation run. This method is unit tested and documented.
    - The second method has the same name, without the underscore prefix e.g. "validate_something". This method is used to call
    the validation, and formats the output with the [`validation_output` decorator](#the-validation_output-decorator).

!!!example "Example of a validation method decorated with @validation_output"
    ```py
    @validation_output
    def validate_something(self, some_arg, some_kwarg):
        return self._validate_something(some_arg, some_kwarg)
    ```

## The `validation_output` decorator
The validation output decorator transforms the output of a validation function into a `Validation`*. For this transformation, it is necessary for the validation function to respect the return type `Tuple[bool, Dict[str, Union[str, int, float]]]`.

???note "`Validation`*"
    :::trubrics.validations.dataclass.Validation
