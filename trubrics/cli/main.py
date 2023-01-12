import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import typer
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn

from trubrics.exceptions import MissingConfigPathError  # , MissingTrubricRunFileError
from trubrics.ui.auth import get_trubrics_auth_token, get_trubrics_firebase_auth_api_url
from trubrics.ui.firestore import (
    get_trubrics_firestore_api_url,
    list_projects_in_organisation,
)
from trubrics.ui.trubrics_config import TrubricsConfig
from trubrics.validations.run import TrubricRun, run_trubric

app = typer.Typer()


@app.command()
def init(
    api_key: str = "AIzaSyBeXhMQclnlc02v1DhE2o_jSY2B8g1SC38",
    run_context_path: str = typer.Option(
        ..., prompt="Enter the path to your trubric run .py file (e.g. examples/classification_titanic/trubric_run.py)"
    ),
    user_connected: bool = typer.Option(False, prompt="Do you already have an account with Trubrics?"),
):
    """The CLI `trubrics init` command for initialising trubrics config.

    Args:
        api_key: the key towards
        trubric_config_path: a path to save the .trubrics_config.json to
    """

    if user_connected:
        email = typer.prompt("Enter your user email")
        password = typer.prompt("Enter your user password", hide_input=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Authenticating user...", total=None)

            firebase_auth_api_url = get_trubrics_firebase_auth_api_url(api_key)
            auth = get_trubrics_auth_token(firebase_auth_api_url, email, password)
            if "uid" in auth.keys() and "idToken" in auth.keys():
                firestore_api_url = get_trubrics_firestore_api_url(auth)
            else:
                rprint(auth)
                raise typer.Abort()

            projects = list_projects_in_organisation(firestore_api_url=firestore_api_url, auth=auth)
            print()
            rprint(f"[bold yellow]Welcome {auth['displayName']}[bold yellow] :sunglasses:")
            print()

        if len(projects) > 0:
            for index, project in enumerate(projects):
                rprint(f"[bold green][{index}][/bold green] [green]{project}[/green]")
            project_num = typer.prompt("Select your project (e.g. 0)")

            try:
                project_int = int(project_num)
                if project_int not in list(range(len(projects))):
                    raise ValueError
                else:
                    project_name = projects[project_int]
            except ValueError:
                message = typer.style(
                    f"Project [{project_num}] not recognised."
                    "Please indicate an integer referring to one of the project names"
                    " above.",
                    fg=typer.colors.RED,
                    bold=True,
                )
                typer.echo(message)
                raise typer.Abort()

        trubrics_config = TrubricsConfig(
            run_context_path=run_context_path,
            firebase_auth_api_url=firebase_auth_api_url,
            firestore_api_url=firestore_api_url,
            email=email,
            password=password,
            project=project_name,  # type: ignore
        )
        trubrics_config.save()

        typer.echo(typer.style("Successful authentication with configuration:", fg=typer.colors.GREEN, bold=True))
        trubrics_config.password = "<USER PASSWORD>"
        rprint(trubrics_config.dict())
    else:
        rprint(
            "[bold green]You're all set to save trubrics & feedback locally."
            "Be sure to check out our docs to see how you can leverage the Trubrics Platform.[bold green]"
        )
        trubrics_config = TrubricsConfig(run_context_path=run_context_path).save()


def _framework_callback(value: str):
    if value not in ["gradio", "streamlit", "dash"]:
        raise typer.BadParameter("Only 'gradio', 'dash' or 'streamlit' frameworks are supported.")
    return value


@app.command()
def example_app(framework: str = typer.Option("streamlit", callback=_framework_callback)):
    """Run the titanic user feedback collector app."""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"../example/app_titanic_{framework}.py")
    if framework == "streamlit":
        subprocess.call(["streamlit", "run", filename])
    elif framework in ["gradio", "dash"]:
        subprocess.call(["python3", filename])


def _import_module(module_path: str):
    try:
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        lib = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["module.name"] = lib
        spec.loader.exec_module(lib)  # type: ignore
    except FileNotFoundError as e:
        raise e
    return lib


@app.command()
def run(
    save_ui: bool = False,
    trubric_config_path: str = typer.Option(
        ...,
        prompt=(
            "Enter the path to your trubric config .json file (this file can be generated by running `trubrics init`)"
        ),
    ),
    trubric_output_file_path: str = typer.Option(
        ".", prompt="Enter a path to save your output trubric file. The default path is"
    ),
    trubric_output_file_name: str = typer.Option(
        "my_new_trubric.json", prompt="Enter the file name of your output trubric file. The default file name is"
    ),
):
    """The CLI `trubrics run` command for running trubrics.

    Args:
        trubric_config_path: path to your trubric config .json file \
            (this file can be generated by running `trubrics init`).
        trubric_output_file_path: path to save your output trubric file
        trubric_output_file_name: file name of your output trubric file.
    """
    trubric_config_file_path = Path(trubric_config_path) / ".trubrics_config.json"
    if not trubric_config_file_path.exists():
        raise MissingConfigPathError(
            f"The trubric configuration file '{trubric_config_file_path}' has not been found. Run `trubrics init` to"
            " create file."
        )
    with open(trubric_config_file_path, "r") as file:
        trubrics_config = json.load(file)
    trubric_run_path = trubrics_config["trubric_run_path"]

    tc = _import_module(module_path=trubric_run_path)
    if hasattr(tc, "RUN_CONTEXT"):
        if isinstance(tc.RUN_CONTEXT, TrubricRun):
            run_context = tc.RUN_CONTEXT
        else:
            raise TypeError("'RUN_CONTEXT' attribute must be of type TrubricRun.")
    else:
        raise AttributeError("Trubrics config python module must contain an attribute 'RUN_CONTEXT'.")

    typer.echo(
        typer.style(
            f"Running trubric from file '{trubric_run_path}' with model '{run_context.trubric.model_name}' and"
            f" dataset '{tc.data_context.name}'.",
            fg=typer.colors.BLUE,
        )
    )
    all_validation_results = run_trubric(tr=run_context)
    validations = []
    for validation_result in all_validation_results:
        validations.append(validation_result)

        message_start = f"{validation_result.validation_type} - {validation_result.severity.upper()}"
        completed_dots = (100 - len(message_start)) * "."
        if validation_result.outcome == "pass":
            ending = typer.style("PASSED", fg=typer.colors.GREEN, bold=True)
        else:
            ending = typer.style("FAILED", fg=typer.colors.WHITE, bg=typer.colors.RED)
        message = typer.style(message_start, bold=True) + completed_dots + ending
        typer.echo(message)

    # save new trubric .json
    new_trubric = tc.trubric
    new_trubric.validations = validations
    new_trubric.save_local(path=trubric_output_file_path, file_name=trubric_output_file_name)

    # save new trubric to ui
    if save_ui is True:
        if "user_id" in trubrics_config.keys():
            new_trubric.save_ui(trubric_config_path)
        else:
            typer.echo(
                typer.style(
                    "ERROR: You must authenticate with the trubrics manager by running `trubrics init` to remotely save"
                    " trubrics runs.",
                    fg=typer.colors.RED,
                )
            )


if __name__ == "__main__":
    app()
