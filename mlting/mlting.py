import json
import pandas as pd
import requests


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

    url = "http://localhost:5000"
    headers = {"Content-type": "application/json"}
    requests.post(url + "/tests/v1/add", data=test_json, headers=headers)