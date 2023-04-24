import os
import subprocess
from pathlib import Path
from typing import Optional

import typer
from loguru import logger
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn

from trubrics.cli.run import validate_trubric_run_context
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
def init(
    firebase_api_key: Optional[str] = None,
    firebase_project_id: Optional[str] = None,
    trubrics_user: bool = typer.Option(False, prompt="Do you already have an account with Trubrics?"),
    project_name: Optional[str] = None,
):
    """
    `trubrics init` initialises an environment and authenticates with a Trubrics platform account.
    It does this by storing a `~/.trubrics_config.json` file in the root directory.
    Be guided through the process by answering the prompts, or feed these in programmatically with
    the environment variables `TRUBRICS_CONFIG_EMAIL` and `TRUBRICS_CONFIG_PASSWORD`:

    ```bash
    export TRUBRICS_CONFIG_EMAIL=<your_trubrics_email>
    ```
    ```bash
    export TRUBRICS_CONFIG_PASSWORD=<your_trubrics_password>
    ```
    ```bash
    trubrics init --trubrics-user --project-name <your_project_name>
    ```

    Args:
        firebase_api_key: optional firebase api key
        firebase_project_id: optional firebase project ID
        trubrics_user: boolean of whether the user has a Trubrics account
        project_name: optional project name to initialise
    """
    if firebase_api_key or firebase_project_id:
        if firebase_api_key and firebase_project_id:
            defaults = TrubricsDefaults(firebase_api_key=firebase_api_key, firebase_project_id=firebase_project_id)
        else:
            raise ValueError("Both API key and firebase_project_id are required to change project.")
    else:
        defaults = TrubricsDefaults()

    if trubrics_user:
        email = os.environ.get("TRUBRICS_CONFIG_EMAIL")
        password = os.environ.get("TRUBRICS_CONFIG_PASSWORD")
        if email or password:
            if not email or not password:
                logger.warning(
                    f"{'TRUBRICS_CONFIG_EMAIL' if not email else 'TRUBRICS_CONFIG_PASSWORD'} environment variable is"
                    " not set, asking user for a prompt."
                )
        email = email or typer.prompt("Enter your user email")
        password = password or typer.prompt("Enter your user password", hide_input=True)

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

            rprint(f"\n[bold yellow]Welcome {auth['displayName']}[bold yellow] :sunglasses:\n")

        if project_name:
            if project_name not in projects:
                raise ValueError(
                    f"Project '{project_name}' not found in organisation '{firestore_api_url.split('/')[-1]}'."
                    f" Projects currently available: {projects}."
                )
        else:
            if len(projects) > 0:
                for index, project in enumerate(projects):
                    rprint(f"[bold green][{index}][/bold green] [green]{project}[/green]")
                project_num = typer.prompt("Select your project (e.g. 0)")

                project_int = int(project_num)
                if project_int not in list(range(len(projects))):
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
                    project_name = projects[project_int]
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
            password=password,  # type: ignore
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
def example_app(
    framework: str = typer.Option("streamlit", callback=_framework_callback),
    trubrics_platform_auth: Optional[str] = None,
):
    """Runs the example user feedback collector app.

    Args:
        framework: framework of streamlit, dash or gradio
        trubrics_platform_auth: whether to save feedback to the Trubrics platform
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"../example/app_titanic_{framework}.py")
    if trubrics_platform_auth not in [None, "single_user", "multiple_users"]:
        raise ValueError(
            f"trubrics_platform_auth={trubrics_platform_auth} not recognised. Must be one of [None, 'single_user',"
            " 'multiple_users']."
        )
    if framework == "streamlit":
        if trubrics_platform_auth:
            subprocess.call(["streamlit", "run", filename, "--", "--trubrics-platform-auth", trubrics_platform_auth])
        else:
            subprocess.call(["streamlit", "run", filename])
    elif framework in ["gradio", "dash"]:
        if trubrics_platform_auth:
            raise ValueError("Trubrics auth currently only available with Streamlit.")
        subprocess.call(["python3", filename])


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
        trubrics_config = load_trubrics_config().dict()
        if trubrics_config["email"] is not None:
            new_trubric.save_ui(raise_on_failure=raise_on_failure)
        else:
            typer.echo(
                typer.style(
                    "ERROR: You must authenticate with the Trubrics platform by running `trubrics init` to remotely"
                    " save trubrics runs.",
                    fg=typer.colors.RED,
                )
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
