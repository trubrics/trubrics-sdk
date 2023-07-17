from pathlib import Path

import typer
from rich import print as rprint

app = typer.Typer(pretty_exceptions_show_locals=False)


def version_callback(value: bool):
    if value:
        import trubrics

        typer.echo(trubrics.__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
):
    return None


@app.command()
def run(
    save_ui: bool = typer.Option(False, prompt="Would you like to save your trubric to the UI?"),
    run_context_path: str = typer.Option(
        default="example", prompt="Enter the path to your trubric run .py file. Press enter for an"
    ),
    trubric_output_file_path: str = "./my_new_trubric.json",
    raise_on_failure: bool = True,
):
    """Runs an example trubric (list of model validations) on the titanic dataset.

    Args:
        save_ui: whether to save validations to the UI with in app user authentication
        run_context_path: path to the trubrics run context
        trubric_output_file_path: path to save your output trubric file
        raise_on_failure: raise an exception on failure of trubric
    """
    from trubrics.cli.run import validate_trubric_run_context
    from trubrics.trubrics_platform.trubrics_config import TrubricsDefaults

    trubric_run_path = None
    if run_context_path != "example":
        trubric_run_path = Path(run_context_path).absolute()
        if not trubric_run_path.exists():
            rprint(f"[red]Path '{trubric_run_path}' not found.[red]")
            raise typer.Abort()
        rc = validate_trubric_run_context(str(trubric_run_path)).RUN_CONTEXT
    else:
        from trubrics.example.trubric_run import RUN_CONTEXT as rc  # type: ignore
    rprint(
        f"\nRunning trubric from file '{trubric_run_path or 'trubrics.example.trubric_run'}' with model"
        f" '{rc.model_name}' and dataset '{rc.data_context.name}'.\n"
    )
    new_trubric = rc.set_new_trubric()
    if save_ui:
        raise NotImplementedError(
            "It is currently not possible to save validations to Trubrics. Get in touch with us if this is an issue."
        )
    else:
        defaults = TrubricsDefaults()
        new_trubric.save_local(trubric_output_file_path, raise_on_failure=raise_on_failure)
        rprint(
            "\n[bold orange_red1]Be sure to check out our docs to see how you can leverage the Trubrics platform."
            f"\n\n{defaults.demo_sign_up_url}[bold orange_red1]\n"
        )


if __name__ == "__main__":
    app()
