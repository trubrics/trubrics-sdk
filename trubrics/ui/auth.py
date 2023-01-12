import json

import requests  # type: ignore


def get_trubrics_firebase_auth_api_url(firebase_api_key):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"


def get_trubrics_auth_token(firebase_auth_api_url, email, password):
    auth_response = json.loads(
        requests.post(
            firebase_auth_api_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"email": email, "password": password, "returnSecureToken": True}),
        ).text
    )
    return {"idToken": auth_response["idToken"], "uid": auth_response["localId"]}