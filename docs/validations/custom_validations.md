# Building custom validations
All ML projects are unique, and custom validations should strongly be considered from the start. They
allow you to tailor trubrics to your needs, and transform user feedback into meaningful validations.
The `ModelValidator` object can be used to build your own custom validations, by creating a class that inherits from
`ModelValidator` as per the example:

!!!example
    ```py
    --8<-- "examples/validations/classification_titanic/custom_validator.py"
    ```

## Software conventions of the `ModelValidator`
For best practices on creating a CustomValidator, follow the same conventions as the `ModelValidator`:

- Contains all code for validations
- All validation names start with the prefix "validate_"
- Validations are built with two methods:
    - A method with an underscored prefix e.g. "_validate_something". This method contains all code logic for the validation,
    and must return a boolean variable that indicates a pass / fail of the validation, and a dictionary that holds
    contextual information that is calculated during the validation run. This method is unit tested and documented.
    - The second method has the same name, without the underscore prefix e.g. "validate_something". This method is used to call the validation, and formats the output with the [`validation_output` decorator](#the-validation_output-decorator).


## The @validation_output decorator

!!!example "Example of a validation method decorated with @validation_output"
    ```py
    @validation_output
    def validate_something(self, some_arg, some_kwarg):
        return self._validate_something(some_arg, some_kwarg)
    ```

The @validation_output decorator transforms the output of a validation function into a `Validation`*. For this transformation, it is necessary for the validation function to respect the return type (outcome, result) -> `Tuple[bool, Dict[str, Union[str, int, float]]]`, where the outcome represents whether the validation has passed or fail, and the result is any metadata that has been computed during the validation that can be useful for giving greater context as to why a validation has passed or failed.

!!!note "*Validation"
    :::trubrics.validations.dataclass.Validation
