import os
from typing import Optional

from pydantic import BaseModel, SecretStr


class TrubricsDefaults(BaseModel):
    # no stress, this is not a secret api key
    firebase_api_key: str = "AIzaSyAB-ldUv6X2rgyN_Jda9EC_AzLkENjoDk8"
    firebase_project_id: str = "trubrics-ea-staging"
    trubrics_url: str = "https://st.ea.trubrics.com/"
    demo_sign_up_url: str = "https://trubrics.com/demo/"


class TrubricsConfig(BaseModel):
    firebase_auth_api_url: Optional[str] = None
    firestore_api_url: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[SecretStr] = None
    project: Optional[str] = None

    class Config:
        json_encoders = {SecretStr: lambda v: v.get_secret_value() if v else None}

    def save(self):
        config_path = os.path.join(os.path.expanduser("~"), ".trubrics_config.json")
        with open(config_path, "w") as file:
            file.write(self.json(indent=4))


def load_trubrics_config() -> TrubricsConfig:
    config_path = os.path.join(os.path.expanduser("~"), ".trubrics_config.json")
    if os.path.exists(config_path):
        return TrubricsConfig.parse_file(config_path)
    else:
        raise FileNotFoundError("Trubrics config file not found. Run `trubrics init` to generate this file.")
