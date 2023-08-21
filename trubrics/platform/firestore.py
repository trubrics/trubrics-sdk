"""
File of HTTP requests to Firestore Rest API.
"""
import json
from datetime import datetime

import requests  # type: ignore
from loguru import logger

from trubrics.platform.auth import expire_after_n_seconds, get_trubrics_auth_token
from trubrics.platform.config import TrubricsConfig
from trubrics.platform.feedback import Feedback


def dict_to_firestore_document(python_dict):
    firestore_compatible = {"fields": {}}
    for key, value in python_dict.items():
        if value is None:
            firestore_compatible["fields"][key] = {"nullValue": value}
        elif isinstance(value, str):
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
            firestore_compatible["fields"][key] = {"mapValue": dict_to_firestore_document(value)}
        elif isinstance(value, list):
            array_values = []
            for item in value:
                if value is None:
                    array_values.append({"nullValue": item})
                elif isinstance(item, str):
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
                    array_values.append({"mapValue": dict_to_firestore_document(item)})
            firestore_compatible["fields"][key] = {"arrayValue": {"values": array_values}}
    return firestore_compatible


def get_trubrics_firestore_api_url(auth, gcp_project_id):
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
            f"https://firestore.googleapis.com/v1/projects/{gcp_project_id}/databases/(default)/documents:runQuery",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
            data=json.dumps(structured_query),
        ).text
    )[0]["document"]["name"]
    return f"https://firestore.googleapis.com/v1/{organisation_route}"


def list_projects_in_organisation(firestore_api_url, auth):
    r = requests.get(
        firestore_api_url + "/projects" + "?pageSize=50",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
    )
    r.raise_for_status()
    projects_res = json.loads(r.text)

    all_projects = []
    if len(projects_res) != 0:
        for component in projects_res["documents"]:
            if component.get("fields", {}).get("archived", {}).get("booleanValue", {}) is False:
                all_projects.append(component["name"].split("/")[-1])
    return all_projects


def list_components_in_organisation(firestore_api_url, auth, project):
    r = requests.get(
        firestore_api_url + f"/projects/{project}/feedback" + "?pageSize=50",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
    )
    r.raise_for_status()
    components_res = json.loads(r.text)

    all_components = []
    if len(components_res) != 0:
        for component in components_res["documents"]:
            if component.get("fields", {}).get("archived", {}).get("booleanValue", {}) is False:
                all_components.append(component["name"].split("/")[-1])
    return all_components


def record_feedback(auth, firestore_api_url, project, document):
    url = firestore_api_url + f"/projects/{project}/feedback/{document.component_name}/responses"
    res = json.loads(
        requests.post(
            url,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {auth['idToken']}"},
            data=json.dumps(dict_to_firestore_document(document.dict())),
        ).text
    )
    from loguru import logger

    logger.info(res["name"].split("/")[-1])
    return res


def save_to_trubrics(trubrics_config: TrubricsConfig, feedback: Feedback) -> dict:
    auth = get_trubrics_auth_token(
        trubrics_config.firebase_api_key,
        trubrics_config.email,
        trubrics_config.password.get_secret_value(),
        rerun=expire_after_n_seconds(),
    )
    components = list_components_in_organisation(
        firestore_api_url=trubrics_config.firestore_api_url, auth=auth, project=trubrics_config.project
    )
    if feedback.component_name not in components:
        raise ValueError(f"Component '{feedback.component_name}' not found. Please select one of: {components}.")
    res = record_feedback(
        auth,
        firestore_api_url=trubrics_config.firestore_api_url,
        project=trubrics_config.project,
        document=feedback.dict(),
    )
    if "error" in res:
        logger.error(res["error"])
    else:
        logger.info("Feedback response saved to Trubrics.")

    return res
