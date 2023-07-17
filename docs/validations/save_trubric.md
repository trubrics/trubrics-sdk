# Save validations as a trubric

!!!warning "trubrics>1.4.2"
    Validations in Trubrics will soon be moved to another repository. For trubrics>1.4.2 users, please install all validations dependencies with:
    ```
    pip install "trubrics[validations]"
    ```

A `Trubric` is a list of validations that represents the gold standard a model must conform to. It also holds metadata about the [model](models.md) and [DataContext](data_context.md) that it has been run against. Once a `Trubric` has been saved (as .json), it can then be rerun against any other [model](models.md) and [DataContext](data_context.md) combination.

## 1. Save a Trubric

Once an ensemble of validations have been built, the list can be input into the `Trubric` object and saved as a local .json file with the `.save_local()` method, and can be saved to the Trubrics platform with the `.save_ui()` method.

!!!tip "Trubrics platform access"
    Saving trubric runs to the Trubrics platform will allow full tracking of the evolution of validations, and sorting runs into projects. Teams within an organisation can push trubric runs to projects. Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access to the Trubrics platform for you and your team.

!!!example

    ```py
    from trubrics.validations import Trubric

    trubric = Trubric(
        name="my_first_trubric",
        model_name="my_model",
        model_version="v0.0.1",
        data_context_name=data_context.name,
        data_context_version=data_context.version,
        tags=["master"],
        validations=validations,  # a list of validations generated from the ModelValidator
    )
    trubric.save_local()  # optional path= parameter to specify a location to save the trubric
    trubric.save_ui()
    ```

You are in charge of versioning your [model](models.md) and [DataContext](data_context.md), and feeding in these values into the `Trubric` to keep track.

!!!tip "Trubric object"
    :::trubrics.validations.dataclass.Trubric

## 2. Run a saved Trubric

Saved `Trubric`s can be run from the [CLI](trubrics_cli.md) or directly from a python environment (notebook, script, ipython kernel, etc):

!!!example

    ```py
    from trubrics.validations.run import TrubricRun

    trubric_run_context = TrubricRun(
        data_context=data_context,
        model=model,
        trubric=Trubric.parse_file("./my_first_trubric.json"),
        custom_validator=CustomValidator,
        custom_scorers=custom_scorers,
        slicing_functions=slicing_functions
    )
    new_trubric = trubric_run_context.set_new_trubric()

    # save new trubric .json locally or to UI
    new_trubric.save_local()
    new_trubric.save_ui()
    ```

!!!tip "TrubricRun object"
    :::trubrics.validations.run.TrubricRun
