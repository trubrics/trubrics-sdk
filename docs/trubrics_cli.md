# Running trubrics from the CLI

Once you have built a trubric of validations, you will want to test different data / models against that trubric.
This will help you to ensure safe deployment of newly trained models directly from CI/CD/CT pipelines.

Don't hesitate to get in touch with us [here](https://trubrics.com/demo/) to gain access to the Trubrics platform. This will allow you to track all trubric runs, and to close feedback issues by linking to specific runs.

Complete these three steps to run trubrics from the CLI tool:

## 1. Create python runner script

Create a python file `<trubric_run_file>.py` that loads datasets / models to validate and holds the necessary code to run all validations. This file must contain a `RUN_CONTEXT` variable with a value of `TrubricRun`, as in the example below. It is this `RUN_CONTEXT` variable that is read into the CLI tool at runtime.

???example "Example of `<trubric_run_file>.py`"
    ```python
        ---8<-- "examples/classification_titanic/trubric_run.py"
    ```

    !!!tip "TrubricRun object"
        :::trubrics.validations.run.TrubricRun

## 2. Initialise an environment with `trubrics init`

Initialise a run config in the terminal to save a `~/.trubrics_config.json` file to your user's root directory. Be guided by the CLI prompts by running:

<p align="center"><img src="../assets/trubrics-init.gif"/></p>

???tip "What is the `.trubrics_config.json`?"
    The trubrics config holds the path to the python runner script created in [step 1](#1-create-python-runner-script), and any credentials for logging to Trubrics.

## 3. Run validations and save locally or to Trubrics

Run all validations from the terminal. This command also saves a new trubric .json with each validation's new outcome and results to a given path. Be guided by the CLI prompts by running:

<p align="center"><img src="../assets/trubrics-run.gif"/></p>

:::trubrics.cli.main.run
