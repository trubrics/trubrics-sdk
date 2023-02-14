import os
from typing import Optional

from pydantic import BaseModel, SecretStr


class TrubricsConfig(BaseModel):
    run_context_path: str
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
        raise Exception("Config file not found.")
