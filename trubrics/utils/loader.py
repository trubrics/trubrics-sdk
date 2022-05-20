import json
from typing import Optional, Union

import pandas as pd
import requests  # type: ignore


def save_test_to_json(
    test: str,
    description: Optional[str],
    prediction: Union[str, int],
    df: pd.DataFrame,
    corrected_prediction: Union[str, int, float, None] = None,
    tracking: bool = False,
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
            "demo/data/trubrics_test.json",
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
            "../data/trubrics_test.json",
            "r",
        ) as file:
            saved_test = json.load(file)
            return pd.DataFrame(saved_test.get("features")), saved_test.get("corrected_prediction")
