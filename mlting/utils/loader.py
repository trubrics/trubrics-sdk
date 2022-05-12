import json

import pandas as pd
import requests


def save_test_to_json(
    test: str,
    description: str,
    prediction: str,
    df: pd.DataFrame,
    corrected_prediction=None,
    tracking=False,
) -> None:
    test_json = json.dumps(
        {
            "test": {
                "name": test,
                "description": description,
            },
            "prediction": prediction,
            "corrected_prediction": corrected_prediction,
            "features": df.to_dict(),
        }
    )
    if tracking:
        url = "http://localhost:5000"
        headers = {"Content-type": "application/json"}
        requests.post(
            url + "/tests/v1/add",
            data=test_json,
            headers=headers,
        )
    else:
        with open(
            "assets/data/mlting_test.json",
            "w",
        ) as file:
            file.write(test_json)


def get_business_test_data(
    tracking: bool = False,
):
    if tracking:
        raise Exception("to be replaced with read from test tracking API")
    else:
        with open(
            "../assets/data/mlting_test.json",
            "r",
        ) as file:
            saved_test = json.load(file)
            return pd.DataFrame(saved_test.get("features")), saved_test.get("corrected_prediction")
