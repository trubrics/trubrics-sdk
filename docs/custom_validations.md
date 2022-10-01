# Building custom validations
All ML projects are unique, and custom validations should strongly be considered from the start. They
allow you to tailor trubrics to your needs, and transform user feedback into meaningful validations.
The `ModelValidator` object can be used to build your own custom validations. Create a class and inherit from
`ModelValidator`, feeding in your DataContext and a [model](models.md).

For best practices on creating a CustomValidator, follow the same conventions as [the `ModelValidator` object](validator_object.md) that are displayed in this example:

!!!example
    ```py
    --8<-- "examples/classification_titanic/custom_validator.py"
    ```
