# Running trubrics
Once you have built a trubric of validations, you will want to test different data / models against that trubric.
This will help you to ensure safe deployment of newly trained models directly from you CI/CD/CT pipelines. To run your
saved trubric from the CLI, you will need to create a python file `<trubrics_config_file>.py` that that holds your DataContext, ModelContext and any
custom validators you may have used. Then run:

--8<-- "docs/snippets/trubrics_cli.md"

The <trubrics_config_file>.py must contain the `TrubricRun*` context as a variable `RUN_CONTEXT`. The CLI tool reads `RUN_CONTEXT`
to execute the trubric on the specified model & data. An example of this file can be seen (and tested) in `examples/trubrics_config.py`.

!!!note "*TrubricRun Context"
    :::trubrics.validators.run_context.TrubricRun
