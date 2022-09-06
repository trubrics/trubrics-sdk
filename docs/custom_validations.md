# Building custom validations
All ML projects are unique, and custom validations should strongly be considered from the start. They
allow you to tailor trubrics to your needs, and transform user feedback into meaningful validations.
The `Validator` object can be used to build your own custom validations. Create a class and inherit from
`Validator`, feeding in DataContext and ModelContext.

!!!example
    :::examples.cli.custom_validator

As seen in the example source code above, the conventions follow those of [the `Validator` object](validator_object.md).
