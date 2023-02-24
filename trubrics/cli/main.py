import os
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn

from trubrics.cli.run import generate_new_trubric, validate_trubric_run_context
from trubrics.ui.auth import get_trubrics_auth_token, get_trubrics_firebase_auth_api_url
from trubrics.ui.firestore import (
    get_trubrics_firestore_api_url,
    list_projects_in_organisation,
)
from trubrics.ui.trubrics_config import (
    TrubricsConfig,
    TrubricsDefaults,
    load_trubrics_config,
)

app = typer.Typer()


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
def init(
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    user_connected: bool = typer.Option(False, prompt="Do you already have an account with Trubrics?"),
):
    """The CLI `trubrics init` command for initialising trubrics config.

    Args:
        api_key: the firebase api key
        project_id: the firebase project ID
    """
    if api_key or project_id:
        if not api_key or not project_id:
            raise Exception("API key and project_id must be input to change project.")
        defaults = TrubricsDefaults(firebase_api_key=api_key, firebase_project_id=project_id)
    else:
        defaults = TrubricsDefaults()

    if user_connected:
        email = typer.prompt("Enter your user email")
        password = typer.prompt("Enter your user password", hide_input=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Authenticating user...", total=None)

            firebase_auth_api_url = get_trubrics_firebase_auth_api_url(defaults.firebase_api_key)
            auth = get_trubrics_auth_token(firebase_auth_api_url, email, password)
            if "error" in auth:
                rprint(f"Error in login email '{email}' to the Trubrics UI: {auth['error']}")
                raise typer.Abort()
            else:
                firestore_api_url = get_trubrics_firestore_api_url(auth, defaults.firebase_project_id)

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
        else:
            message = typer.style(
                f"Organisation '{firestore_api_url.split('/')[-1]}' has no projects created."
                " Navigate to the Trubrics UI to add a project.",
                fg=typer.colors.RED,
                bold=True,
            )
            typer.echo(message)
            raise typer.Abort()

        trubrics_config = TrubricsConfig(
            firebase_auth_api_url=firebase_auth_api_url,
            firestore_api_url=firestore_api_url,
            username=auth["displayName"],
            email=email,
            password=password,
            project=project_name,  # type: ignore
        )
        trubrics_config.save()

        typer.echo(typer.style("Successful authentication with configuration:", fg=typer.colors.GREEN, bold=True))
        rprint(trubrics_config.dict())
        rprint()
        rprint(
            "[bold green]You can now push trubrics and feedback to the Trubrics platform:"
            f"\n{defaults.trubrics_url}[bold green]\n"
        )
    else:
        rprint(
            "[bold orange_red1]Sign up here to get access to the Trubrics platform:"
            f"\n\n{defaults.demo_sign_up_url}[bold orange_red1]\n"
        )


def _framework_callback(value: str):
    if value not in ["gradio", "streamlit", "dash"]:
        raise typer.BadParameter("Only 'gradio', 'dash' or 'streamlit' frameworks are supported.")
    return value


@app.command()
def example_app(framework: str = typer.Option("streamlit", callback=_framework_callback), save_ui: bool = False):
    """Run the titanic user feedback collector app."""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"../example/app_titanic_{framework}.py")
    if framework == "streamlit":
        if save_ui:
            subprocess.call(["streamlit", "run", filename, "--", "--save-ui"])
        else:
            subprocess.call(["streamlit", "run", filename])
    elif framework in ["gradio", "dash"]:
        subprocess.call(["python3", filename])


@app.command()
def run(
    save_ui: bool = typer.Option(False, prompt="Would you like to save you trubric to the UI?"),
    run_context_path: str = typer.Option(
        "examples/classification_titanic/trubric_run.py", prompt="Enter the path to your trubric run .py file"
    ),
    trubric_output_file_path: str = typer.Option(
        "./my_new_trubric.json", prompt="Enter a local path to save your output trubric file. Press enter for default"
    ),
):
    """The CLI `trubrics run` command for running trubrics.

    Args:
        save_ui: save trubric to ui.
        trubric_output_file_path: path to save your output trubric file
    """
    trubric_run_path = Path(run_context_path).absolute()
    if not trubric_run_path.exists():
        rprint(f"[red]Path '{trubric_run_path}' not found.[red]")
        raise typer.Abort()

    tc = validate_trubric_run_context(str(trubric_run_path))
    rprint(
        f"\nRunning trubric from file '{trubric_run_path}' with model '{tc.RUN_CONTEXT.trubric.model_name}' and dataset"
        f" '{tc.data_context.name}'.\n"
    )
    new_trubric = generate_new_trubric(tc)
    if save_ui:
        trubrics_config = load_trubrics_config().dict()
        if trubrics_config["email"] is not None:
            new_trubric.save_ui()
        else:
            typer.echo(
                typer.style(
                    "ERROR: You must authenticate with the trubrics manager by running `trubrics init` to remotely save"
                    " trubrics runs.",
                    fg=typer.colors.RED,
                )
            )
    else:
        defaults = TrubricsDefaults()
        new_trubric.save_local(trubric_output_file_path)
        rprint(
            "\n[bold orange_red1]Be sure to check out our docs to see how you can leverage the Trubrics platform."
            f"\n\n{defaults.demo_sign_up_url}[bold orange_red1]\n"
        )


if __name__ == "__main__":
    app()
