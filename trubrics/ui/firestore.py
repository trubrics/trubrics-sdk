"""
File of HTTP requests to Firestore Rest API.
"""
import json
from datetime import datetime

import requests  # type: ignore


def json_to_firestore_document(json_object):
    python_dict = json.loads(json_object)
    firestore_compatible = {"fields": {}}
    for key, value in python_dict.items():
        if isinstance(value, str):
            firestore_compatible["fields"][key] = {"stringValue": value}
        elif isinstance(value, int):
            firestore_compatible["fields"][key] = {"integerValue": value}
        elif isinstance(value, float):
            firestore_compatible["fields"][key] = {"doubleValue": value}
        elif isinstance(value, bool):
            firestore_compatible["fields"][key] = {"booleanValue": value}
        elif isinstance(value, datetime):
            firestore_compatible["fields"][key] = {"timestampValue": value.isoformat() + "Z"}
        elif isinstance(value, dict):
            firestore_compatible["fields"][key] = {"mapValue": json_to_firestore_document(json.dumps(value))}
        elif isinstance(value, list):
            array_values = []
            for item in value:
                if isinstance(item, str):
                    array_values.append({"stringValue": item})
                elif isinstance(item, int):
                    array_values.append({"integerValue": item})
                elif isinstance(item, float):
                    array_values.append({"doubleValue": item})
                elif isinstance(item, bool):
                    array_values.append({"booleanValue": item})
                elif isinstance(item, datetime):
                    array_values.append({"timestampValue": item.isoformat() + "Z"})
                elif isinstance(item, dict):
                    array_values.append({"mapValue": json_to_firestore_document(json.dumps(item))})
            firestore_compatible["fields"][key] = {"arrayValue": {"values": array_values}}
    return firestore_compatible


def get_trubrics_firestore_api_url(auth, auth_token):
    structured_query = {
        "structuredQuery": {
            "from": [{"collectionId": "organisations"}],
            "select": {"fields": [{"fieldPath": auth["uid"]}]},
        }
    }
    organisation_route = json.loads(
        requests.post(
            "https://firestore.googleapis.com/v1/projects/trubrics-ea-dev/databases/(default)/documents:runQuery",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"},
            data=json.dumps(structured_query),
        ).text
    )[0]["document"]["name"]
    return f"https://firestore.googleapis.com/v1/{organisation_route}"