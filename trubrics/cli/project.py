import typer

app = typer.Typer(help="Manage your projects.")


@app.command()
def create(name: str):
    typer.echo(f"WIP: Project {name} created.")


@app.command()
def delete(name: str):
    typer.echo(f"WIP: Project {name} deleted.")


if __name__ == "__main__":
    app()
