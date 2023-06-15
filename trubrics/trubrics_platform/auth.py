import json
import time
from functools import lru_cache
from typing import Dict, Optional

import requests  # type: ignore
from loguru import logger

from trubrics.trubrics_platform.firestore import (
    get_trubrics_firestore_api_url,
    list_components_in_organisation,
)
from trubrics.trubrics_platform.trubrics_config import TrubricsConfig, TrubricsDefaults


def get_trubrics_firebase_auth_api_url(firebase_api_key):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"


def expire_after_n_seconds(seconds=600):
    """Return the same value within `seconds` time period."""
    return round(time.time() / seconds)


@lru_cache(maxsize=32)
def get_trubrics_auth_token(firebase_auth_api_url, email, password, rerun=None) -> Dict[str, str]:
    del rerun  # this variable is just used to force a refresh of lru_cache
    try:
        r = requests.post(
            firebase_auth_api_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"email": email, "password": password, "returnSecureToken": True}),
            timeout=5000,
        )
        r.raise_for_status()
        auth_response = json.loads(r.text)

        return {
            "idToken": auth_response["idToken"],
            "email": auth_response["email"],
            "uid": auth_response["localId"],
            "displayName": auth_response["displayName"],
        }
    except requests.exceptions.RequestException as err:
        return {"error": str(err)}


def init_platform(
    component_name: str,
    email: str,
    password: str,
    firebase_api_key: Optional[str] = None,
    firebase_project_id: Optional[str] = None,
):
    if firebase_api_key or firebase_project_id:
        if firebase_api_key and firebase_project_id:
            defaults = TrubricsDefaults(firebase_api_key=firebase_api_key, firebase_project_id=firebase_project_id)
        else:
            raise ValueError("Both API key and firebase_project_id are required to change project.")
    else:
        defaults = TrubricsDefaults()

    firebase_auth_api_url = get_trubrics_firebase_auth_api_url(defaults.firebase_api_key)
    auth = get_trubrics_auth_token(firebase_auth_api_url, email, password, rerun=expire_after_n_seconds())
    if "error" in auth:
        raise Exception(f"Error in login email '{email}' to the Trubrics UI: {auth['error']}")
    else:
        firestore_api_url = get_trubrics_firestore_api_url(auth, defaults.firebase_project_id)

    components = list_components_in_organisation(firestore_api_url=firestore_api_url, auth=auth)
    if component_name not in components:
        raise ValueError(
            f"Component '{component_name}' not found in organisation '{firestore_api_url.split('/')[-1]}'."
            f" Components currently available: {components}."
        )

    if "error" in auth:
        error_msg = f"Error in pushing feedback issue with email '{email}' to the Trubrics UI: {auth['error']}"
        logger.error(error_msg)
        raise Exception(error_msg)
    else:
        logger.info(f"User {email} has been authenticated.")
        return TrubricsConfig(
            email=email,
            password=password,  # type: ignore
            username=auth["displayName"],
            firebase_auth_api_url=firebase_auth_api_url,
            firestore_api_url=firestore_api_url,
        )
