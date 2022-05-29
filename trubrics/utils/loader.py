import json

import requests  # type: ignore

from trubrics.context import TrubricContext


def save_test_to_json(trubric_context: TrubricContext, tracking: bool = False) -> None:
    test_json = trubric_context.json()
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
) -> TrubricContext:
    if tracking:
        raise Exception("to be replaced with read from test tracking API")
    else:
        with open(
            "../data/trubrics_test.json",
            "r",
        ) as file:
            saved_test = json.load(file)
            return saved_test
