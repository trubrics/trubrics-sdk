# Save validations as a trubric
A `Trubric` is a list of validations that represents the gold standard a model must conform to. It also holds metadata about the [model](models.md) and [DataContext](data_context.md) that it has been run against. Once a `Trubric` has been saved (as .json), it can then be rerun against any other [model](models.md) and [DataContext](data_context.md) combination.

## 1. Save a Trubric
Once an ensemble of validations have been built, the list can be input into the `Trubric` object and saved as a local .json file with the `.save_local()` method.

!!!example

    ```py
    from trubrics.validations import Trubric

    trubric = Trubric(
        trubric_name="my_first_trubric",
        model_name="my_model",
        model_version=0.1,
        data_context_name=data_context.name,
        data_context_version=data_context.version,
        metadata={"tag": "master"},
        validations=validations,  # a list of validations generated from the ModelValidator
    )
    trubric.save_local(path=".")
    ```

You are in charge of versioning your [model](models.md) and [DataContext](data_context.md), and feeding in these values into the `Trubric` to keep track.

!!!tip "Trubric object"
    :::trubrics.validations.dataclass.Trubric

## 2. Run a saved Trubric
Saved `Trubric`s can be run from the [CLI](trubrics_cli.md) or directly from a python environment (notebook, script, ipython kernel, etc):

!!!example

    ```py
    from trubrics.validations.run import TrubricRun, run_trubric

    trubric_run_context = TrubricRun(
        data_context=data_context,
        model=model,
        trubric=Trubric.parse_file("./my_first_trubric.json"),
        custom_validator=CustomValidator,
        custom_scorers=custom_scorers,
        slicing_functions=slicing_functions
    )
    all_validation_results = run_trubric(trubric_run_context)

    new_validations = []
    for validation_result in all_validation_results:
        print(validation_result.validation_type, validation_result.severity, validation_result.outcome)
        new_validations.append(validation_result)

    # save new trubric .json
    new_trubric = trubric_run_context.trubric
    new_trubric.validations = validations
    new_trubric.save_local(path=".", file_name="my_new_trubric.json")
    ```

The example above makes use of the `TrubricRun` object, and a `run_trubric` generator function.
!!!tip "TrubricRun object"
    :::trubrics.validations.run.TrubricRun
