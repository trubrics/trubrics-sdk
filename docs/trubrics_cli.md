# The Trubrics CLI

The CLI tool allows users to:

1. Connect to the Trubrics platform with [`trubrics init`](#1-trubrics-init). Once connected, all feedback and validations may be saved directly to the platform.
2. Run a set of validations against a model / dataset with [`trubrics run`](#2-trubrics-run). This is allows for validations to be run in an automated pipeline (CI/CD/CT).

!!!tip "Trubrics platform access"
    This will allow you and your team to track all trubric runs in projects, and to close feedback issues by linking to specific runs. Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access to the Trubrics platform for you and your team.


## 1. `trubrics init`

<p align="center"><img src="../assets/trubrics-init.gif"/></p>

:::trubrics.cli.main.init

## 2. `trubrics run`

#### 2.1 Create python runner script

Create a python file `<trubric_run_file>.py` that loads datasets / models to validate and holds the necessary code to run all validations. This file must contain a `RUN_CONTEXT` variable with a value of `TrubricRun`, as in the example below. It is this `RUN_CONTEXT` variable that is read into the CLI tool at runtime.

!!!example "Example of `<trubric_run_file>.py`"
    ```py
    import joblib
    from trubrics.validations import DataContext
    from trubrics.validations.run import TrubricRun

    RUN_CONTEXT = TrubricRun(
        data_context=DataContext(...),  # new data context
        model=joblib.load(...),  # new model
        trubric=Trubric.parse_file(...)
    )
    ```

    ## TrubricRun Object
    ::: trubrics.validations.run.TrubricRun

#### 2.2 Run validations and save locally or to Trubrics

Run all validations from the terminal. This command also saves a new trubric .json with each validation's new outcome and results to a given path. Either save this trubric locally with `--no-save-ui` or to the Trubrics platform with `--save-ui`.

Be guided by the CLI prompts by running:

<p align="center"><img src="../assets/trubrics-run.gif"/></p>

!!!example "Run trubric with titanic example"
    You can test the `trubrics run` command with our titanic example model on 5 saved validations.
    Use `--save-ui` to save this example trubric to the Trubrics platform.
    ```console
    (venv)$ trubrics run --no-save-ui \
    --run-context-path titanic-example-trubric \
    --trubric-output-file-path "my_trubric.json"
    ```


:::trubrics.cli.main.run
