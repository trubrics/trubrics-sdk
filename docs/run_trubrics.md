# Running trubrics
Once you have built a trubric of validations, you will want to test different data / models against that trubric.
This will help you to ensure safe deployment of newly trained models directly from CI/CD/CT pipelines. To run a
saved trubric from the CLI, you will need to create a python file `<trubrics_config_file>.py` that holds the path to your saved trubric, a `DataContext`, a model, and any custom validator you may have used. An example of this file can be seen (and tested) in `examples/classification_titanic/trubric_run.py`. To run this example:
---8<-- "docs/snippets/trubrics_cli.md"

-----

::: trubrics.cli.main.run

-----

:::trubrics.validations.run.TrubricRun
