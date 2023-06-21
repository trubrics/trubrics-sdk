import json
import time
from functools import lru_cache
from typing import Dict, Optional

import requests  # type: ignore
from loguru import logger

from trubrics.trubrics_platform.firestore import get_trubrics_firestore_api_url
from trubrics.trubrics_platform.trubrics_config import TrubricsConfig, TrubricsDefaults


def expire_after_n_seconds(seconds=600):
    """Return the same value within `seconds` time period."""
    return round(time.time() / seconds)


def reset_trubrics_password(firebase_api_key, email) -> Dict[str, str]:
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={firebase_api_key}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"requestType": "PASSWORD_RESET", "email": email}),
            timeout=5000,
        )
        r.raise_for_status()
        auth_response = json.loads(r.text)
        logger.info(f"User password link for {email} has been sent.")
        return auth_response
    except requests.exceptions.RequestException as err:
        logger.error(f"Error sending rest password link for {email}: {str(err)}.")
        return {"error": str(err)}


def create_trubrics_account(firebase_api_key, email, password) -> Dict[str, str]:
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebase_api_key}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"email": email, "password": password}),
            timeout=5000,
        )
        r.raise_for_status()
        auth_response = json.loads(r.text)
        logger.info(f"User account {email} has been created.")
        return auth_response
    except requests.exceptions.RequestException as err:
        logger.error(f"Error creating account for {email}: {str(err)}.")
        return {"error": str(err)}


@lru_cache(maxsize=32)
def get_trubrics_auth_token(firebase_api_key, email, password, rerun=None) -> Dict[str, str]:
    del rerun  # this variable is just used to force a refresh of lru_cache
    try:
        r = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"email": email, "password": password, "returnSecureToken": True}),
            timeout=5000,
        )
        r.raise_for_status()
        auth_response = json.loads(r.text)
        logger.info(f"User {email} has been authenticated.")
        return {
            "idToken": auth_response["idToken"],
            "email": auth_response["email"],
            "uid": auth_response["localId"],
            "displayName": auth_response["displayName"],
        }
    except requests.exceptions.RequestException as err:
        logger.error(f"Error authenticating {email}: {str(err)}.")
        return {"error": str(err)}


def init(
    email: str,
    password: str,
    firebase_api_key: Optional[str] = None,
    firebase_project_id: Optional[str] = None,
) -> TrubricsConfig:
    if firebase_api_key or firebase_project_id:
        if firebase_api_key and firebase_project_id:
            defaults = TrubricsDefaults(firebase_api_key=firebase_api_key, firebase_project_id=firebase_project_id)
        else:
            raise ValueError("Both API key and firebase_project_id are required to change project.")
    else:
        defaults = TrubricsDefaults()

    auth = get_trubrics_auth_token(defaults.firebase_api_key, email, password, rerun=expire_after_n_seconds())
    if "error" in auth:
        raise Exception(f"Error in login email '{email}' to the Trubrics UI: {auth['error']}")
    else:
        firestore_api_url = get_trubrics_firestore_api_url(auth, defaults.firebase_project_id)

    if "error" in auth:
        error_msg = f"Error in pushing feedback issue with email '{email}' to the Trubrics UI: {auth['error']}"
        logger.error(error_msg)
        raise Exception(error_msg)
    else:
        return TrubricsConfig(
            email=email,
            password=password,  # type: ignore
            username=auth["displayName"],
            firebase_api_key=defaults.firebase_api_key,
            firestore_api_url=firestore_api_url,
        )
