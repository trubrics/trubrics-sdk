import importlib.util
import json
import os
import sys

import typer
from rich import print as rprint

from trubrics.utils.trubrics_manager_connector import make_request
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
    Authenticate a User ID with an account created on the trubrics manager UI.
    """
    uid = typer.prompt("Enter your User ID (generated in the trubrics manager)")

    url = "https://trubrics-api-efmcopwrwa-ew.a.run.app"

    res = make_request(f"{url}/api/is_user/{uid}", headers={"Content-Type": "application/json"})
    res = json.loads(res)
    if "is_user" in res.keys():
        message = typer.style(res["msg"], fg=typer.colors.RED, bold=True)
        typer.echo(message)
    else:
        os.environ["TRUBRICS_MANAGER_UID"] = uid
        message = typer.style("User authenticated with the trubrics manager UI:", fg=typer.colors.GREEN, bold=True)
        typer.echo(message)
        rprint(res)


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
