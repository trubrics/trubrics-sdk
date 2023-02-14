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
        elif isinstance(value, bool):
            firestore_compatible["fields"][key] = {"booleanValue": value}
        elif isinstance(value, int):
            firestore_compatible["fields"][key] = {"integerValue": value}
        elif isinstance(value, float):
            firestore_compatible["fields"][key] = {"doubleValue": value}
        elif isinstance(value, datetime):
            firestore_compatible["fields"][key] = {"timestampValue": value.isoformat() + "Z"}
        elif isinstance(value, dict):
            firestore_compatible["fields"][key] = {"mapValue": json_to_firestore_document(json.dumps(value))}
        elif isinstance(value, list):
            array_values = []
            for item in value:
                if isinstance(item, str):
                    array_values.append({"stringValue": item})
                elif isinstance(item, bool):
                    array_values.append({"booleanValue": item})
                elif isinstance(item, int):
                    array_values.append({"integerValue": item})
                elif isinstance(item, float):
                    array_values.append({"doubleValue": item})
                elif isinstance(item, datetime):
                    array_values.append({"timestampValue": item.isoformat() + "Z"})
                elif isinstance(item, dict):
                    array_values.append({"mapValue": json_to_firestore_document(json.dumps(item))})
            firestore_compatible["fields"][key] = {"arrayValue": {"values": array_values}}
    return firestore_compatible


def get_trubrics_firestore_api_url(auth):
    structured_query = {
        "structuredQuery": {
            "from": [{"collectionId": "organisations"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "users"},
                    "op": "ARRAY_CONTAINS",
                    "value": {
                        "stringValue": auth["email"],
                    },
                }
            },
        }
    }
    organisation_route = json.loads(
        requests.post(
            "https://firestore.googleapis.com/v1/projects/trubrics-ea-dev/databases/(default)/documents:runQuery",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
            data=json.dumps(structured_query),
        ).text
    )[0]["document"]["name"]
    return f"https://firestore.googleapis.com/v1/{organisation_route}"


def list_projects_in_organisation(firestore_api_url, auth):
    projects_res = json.loads(
        requests.get(
            firestore_api_url + "/projects",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
        ).text
    )
    return [project["name"].split("/")[-1] for project in projects_res["documents"]] if len(projects_res) != 0 else []


def add_document_to_project_subcollection(auth, firestore_api_url, project, subcollection, document_id, document_json):
    url = firestore_api_url + f"/projects/{project}/{subcollection}/?documentId={document_id}"
    res = json.loads(
        requests.post(
            url,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
            data=json.dumps(json_to_firestore_document(document_json)),
        ).text
    )
    return res
