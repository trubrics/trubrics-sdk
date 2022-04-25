import json
import pandas as pd


def save_test_to_json(
    test: str, description: str, prediction: str, df: pd.DataFrame
) -> None:
    test_json = json.dumps(
        {
            "test": {"name": test, "description": description},
            "prediction": prediction,
            "features": df.to_json(orient="split"),
        }
    )

    with open("assets/data/mlting_test.json", "w") as file:
        file.write(test_json)
