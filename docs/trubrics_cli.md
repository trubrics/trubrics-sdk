# Running trubrics from the CLI

Once you have built a trubric of validations, you will want to test different data / models against that trubric.
This will help you to ensure safe deployment of newly trained models directly from CI/CD/CT pipelines.

!!!tip "Trubrics platform access"
This will allow you and your team to track all trubric runs in projects, and to close feedback issues by linking to specific runs. Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access to the Trubrics platform for you and your team.

Complete these three steps to run trubrics from the CLI tool:

## 1. Create python runner script

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
    :::trubrics.validations.run.TrubricRun

## 2. Connect to the Trubrics platform with `trubrics init`

Initialise a run config in the terminal to save a `~/.trubrics_config.json` file to your user's root directory. This config file holds credentials and connectivity for logging any data to the Trubrics platform. Be guided by the CLI prompts by running:

<p align="center"><img src="../assets/trubrics-init.gif"/></p>

:::trubrics.cli.main.init

## 3. Run validations and save locally or to Trubrics

Run all validations from the terminal. This command also saves a new trubric .json with each validation's new outcome and results to a given path.

!!!example "Run trubric with titanic example"
    ```console
    (venv)$ trubrics run --no-save-ui \
    --run-context-path titanic-example-trubric \
    --trubric-output-file-path "my_trubric.json"
    ```

Or be guided by the CLI prompts by running:

<p align="center"><img src="../assets/trubrics-run.gif"/></p>

:::trubrics.cli.main.run
