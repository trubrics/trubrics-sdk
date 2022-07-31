import importlib.util
import sys

import typer

from trubrics.validators.run import run_trubric
from trubrics.validators.run_context import TrubricRun

app = typer.Typer()


@app.command()
def run(trubric_init_path: str):
    """The CLI `trubrics run` command for running trubrics.

    Example:
        ```
        trubrics run <trubric_init_path>.py
        ```

    Args:
        trubric_init_path: a path towards a .py file that initialises data, model and trubrics contexts.
                           This file must contain the TrubricRun object that holds all contexts to run a
                           trubric. The TrubricRun object must be set to a variable `RUN_CONTEXT` to be recognised.
                           For example `RUN_CONTEXT=TrubricRun(...)`.

    """
    tc = _import_module(module_path=trubric_init_path)
    if hasattr(tc, "RUN_CONTEXT"):
        if isinstance(tc.RUN_CONTEXT, TrubricRun):
            tc = tc.RUN_CONTEXT
        else:
            raise TypeError("'RUN_CONTEXT' attribute must be of type TrubricRun.")
    else:
        raise AttributeError("Trubrics config python module must contain an attribute 'RUN_CONTEXT'.")

    typer.echo(
        typer.style(
            f"Running trubric from file '{trubric_init_path}' with model '{tc.model_context.name}' and dataset"
            f" '{tc.data_context.name}'.",
            fg=typer.colors.BLUE,
        )
    )
    all_validation_results = run_trubric(
        data_context=tc.data_context,
        model_context=tc.model_context,
        trubric=tc.trubric_context,
        custom_validator=tc.custom_validator,
    )
    for validation_result in all_validation_results:
        validation_type, severity, outcome = validation_result

        message_start = f"{validation_type} - {severity.upper()}"
        completed_dots = (100 - len(message_start)) * "."
        if outcome == "pass":
            ending = typer.style("PASSED", fg=typer.colors.GREEN, bold=True)
        else:
            ending = typer.style("FAILED", fg=typer.colors.WHITE, bg=typer.colors.RED)
        message = typer.style(message_start, bold=True) + completed_dots + ending
        typer.echo(message)


@app.command()
def init():
    """
    gcloud init style authorisation to a project created on the trubrics UI.
    """
    typer.echo("WIP: CLI like `gcloud init` to connect to a project on trubrics API.")


def _import_module(module_path: str):
    try:
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        lib = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["module.name"] = lib
        spec.loader.exec_module(lib)  # type: ignore
    except FileNotFoundError as e:
        raise e
    return lib


if __name__ == "__main__":
    app()
