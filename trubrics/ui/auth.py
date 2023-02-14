import json
from typing import Dict

import requests  # type: ignore


def get_trubrics_firebase_auth_api_url(firebase_api_key):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"


def get_trubrics_auth_token(firebase_auth_api_url, email, password) -> Dict[str, str]:
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
