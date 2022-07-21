# Running trubrics
Once you have saved a trubrics file, it is possible to run your trubrics directly from the CLI.

--8<-- "docs/snippets/trubrics_cli.md"

The trubric_config.py above is a file that must contain the TrubricRun context as a variable `RUN_CONTEXT`.
An example of this file can be seen (and tested) in `examples/trubrics_config.py`.

???note "The TrubricRun Context"
    :::trubrics.validators.run_context.TrubricRun
