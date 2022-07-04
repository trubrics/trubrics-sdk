import joblib
import pandas as pd
import typer
from sklearn.metrics import accuracy_score

import trubrics.cli.project as project
from trubrics.context import DataContext, ModelContext, TrubricContext
from trubrics.modellers.classifier import Classifier
from trubrics.validators.base import Validator

app = typer.Typer()
app.add_typer(project.app, name="project")


@app.command()
def run(test_set_path: str, model_path: str, trubric_path: str):
    typer.echo(f"Loading trubric from {trubric_path}.")
    testing_data = pd.read_csv(test_set_path)
    model = joblib.load(model_path)
    data_context = DataContext(testing_data=testing_data, target_column="Survived")
    model_context = ModelContext(
        estimator=model,
        evaluation_function=accuracy_score,
    )
    trubrics_model = Classifier(data=data_context, model=model_context)
    model_validator = Validator(trubrics_model=trubrics_model)
    trubric = TrubricContext.parse_file(trubric_path)
    typer.echo(f"Loaded trubric '{trubric.name}', running validations.")
    for validation in trubric.validations:
        args = validation.validation_kwargs["args"]
        kwargs = validation.validation_kwargs["kwargs"]
        try:
            result = getattr(model_validator, validation.validation_type)(*args, **kwargs)
            message_start = f"{validation.validation_type} - {validation.severity.upper()}"
            completed_dots = (100 - len(message_start)) * "."
            if result.outcome == "pass":
                ending = typer.style("PASSED", fg=typer.colors.GREEN, bold=True)
            else:
                ending = typer.style("FAILED", fg=typer.colors.WHITE, bg=typer.colors.RED)
            message = typer.style(message_start, bold=True) + completed_dots + ending
            typer.echo(message)
        except AttributeError:
            custom_validation = typer.style(
                f"Custom validations like {validation.validation_type} are not yet supported.", fg=typer.colors.YELLOW
            )
            typer.echo(custom_validation)


if __name__ == "__main__":
    app()
