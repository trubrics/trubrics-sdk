import importlib.util
import sys

import typer

import trubrics.cli.project as project
from trubrics.validators.run import run_trubric

app = typer.Typer()
app.add_typer(project.app, name="project")


@app.command()
def run(module_path: str):
    tc = _import_module(module_path=module_path)
    typer.echo(
        typer.style(
            f"Running trubric from '{tc.TRUBRIC_PATH} with model '{tc.MODEL_CONTEXT.name} and dataset"
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
