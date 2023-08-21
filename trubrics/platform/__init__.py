from typing import Optional

from trubrics.platform.auth import expire_after_n_seconds, get_trubrics_auth_token
from trubrics.platform.config import TrubricsConfig, TrubricsDefaults
from trubrics.platform.firestore import (
    get_trubrics_firestore_api_url,
    list_projects_in_organisation,
)


def init(
    email: str,
    password: str,
    project: str,
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

    projects = list_projects_in_organisation(firestore_api_url, auth)
    if project not in projects:
        raise KeyError(f"Project '{project}' not found. Please select one of {projects}.")

    return TrubricsConfig(
        email=email,
        password=password,  # type: ignore
        project=project,
        username=auth["displayName"],
        firebase_api_key=defaults.firebase_api_key,
        firestore_api_url=firestore_api_url,
    )


__all__ = ["init"]
