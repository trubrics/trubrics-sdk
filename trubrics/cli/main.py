import importlib.util
import sys

import typer

import trubrics.cli.project as project
from trubrics.validators.run import run_trubric

app = typer.Typer()
app.add_typer(project.app, name="project")


@app.command()
def run(trubric_init_path: str):
    """
    Specify the TRUBRIC_INIT_PATH that points to your initialisation file.

    For example: trubrics run examples/trubrics_config.py

    This file must contain constant values with:

        - TRUBRIC_PATH: the path towards your .json trubric file that you want to run \n
        - MODEL_CONTEXT: your model context object with the model you would like to test \n
        - DATA_CONTEXT: your data context object with the data you would like to test
    """
    tc = _import_module(module_path=trubric_init_path)
    typer.echo(
        typer.style(
            f"Running trubric from '{tc.TRUBRIC_PATH}' with model '{tc.MODEL_CONTEXT.name}' and dataset"
            f" '{tc.DATA_CONTEXT.name}'.",
            fg=typer.colors.BLUE,
        )
    )
    all_validation_results = run_trubric(
        data_context=tc.DATA_CONTEXT, model_context=tc.MODEL_CONTEXT, trubric_path=tc.TRUBRIC_PATH
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
