import json
import os

from pydantic import BaseModel


class TrubricsConfig(BaseModel):
    firebase_auth_api_url: str
    firestore_api_url: str
    email: str
    password: str
    run_context_path: str
    organisation: str


def save_trubrics_config(config):
    # Save the config to a file in the user's home directory
    config_path = os.path.join(os.path.expanduser("~"), ".trubrics_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f)


def load_trubrics_config():
    # Load the config from the file in the user's home directory
    config_path = os.path.join(os.path.expanduser("~"), ".trubrics_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        raise Exception("Config file not found.")
