import json

import requests  # type: ignore

from trubrics.feedback.dataclass import Feedback


def save_validation_to_json(trubric_context: Feedback, tracking: bool = False) -> None:
    test_json = trubric_context.json()
    if tracking:
        url = "http://localhost:8000"
        headers = {"Content-type": "application/json"}
        requests.post(
            url + "/api/feedback/",
            data=test_json,
            headers=headers,
        )
    else:
        with open(
            "examples/data/feedback.json",
            "w",
        ) as file:
            file.write(test_json)


def get_business_feedback_data(
    tracking: bool = False,
) -> Feedback:
    if tracking:
        raise ValueError("to be replaced with read from test tracking API")
    else:
        with open(
            "../data/feedback_demo.json",
            "r",
        ) as file:
            saved_test = json.load(file)
            return saved_test
