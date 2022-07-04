import typer

import trubrics.cli.project as project

app = typer.Typer()
app.add_typer(project.app, name="project")

if __name__ == "__main__":
    app()
