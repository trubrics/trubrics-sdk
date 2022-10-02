# Running trubrics (CLI)
Once you have built a trubric of validations, you will want to test different data / models against that trubric.
This will help you to ensure safe deployment of newly trained models directly from CI/CD/CT pipelines.

Complete these three steps to run trubrics from the CLI tool:
## 1. Initialise TrubricRun
Create a python file `<trubric_run_file>.py` that loads datasets / models to validate and holds the necessary code to run all validations. This file must contain a `RUN_CONTEXT` variable with a value of `TrubricRun`, as in the example below. It is this `RUN_CONTEXT` variable that is read into the CLI tool at runtime.

???example "Example of `<trubric_run_file>.py`"
    ```py
    ---8<-- "examples/classification_titanic/trubric_run.py"
    ```

    !!!tip "TrubricRun requirements"
    :::trubrics.validations.run.TrubricRun



## 2. Generate run config
Initialise a run config in the terminal to save a `.trubrics_config.json` file to a specified path. Be guided by the CLI prompts by running:

```console
(venv)$ trubrics init
```

::: trubrics.cli.main.init

???tip "What is the `.trubrics_config.json`?"
    The trubrics config holds information about where the code is to run trubrics, and any credentials for logging to the trubrics manager (coming soon).

## 3. Run from CLI
Run all validations from the terminal. Be guided by the CLI prompts by running:

```console
(venv)$ trubrics run
```

::: trubrics.cli.main.run

???example "Run the titanic example"
    If the repository is cloned, you can run this file with the following command from a terminal:
    ```console
    (venv)$ trubrics run \
            --no-save-ui \
            --trubric-config-path "examples/classification_titanic" \
            --trubric-output-file-path "examples/classification_titanic" \
            --trubric-output-file-name "my_new_trubric.json"
    ```
