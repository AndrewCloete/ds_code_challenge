import json
from types import SimpleNamespace
from typing import TypedDict

class S3Secrets(TypedDict):
    access_key: str
    secret_key: str

class Secrets(TypedDict):
    s3: S3Secrets

class SecretsService:
    def __init__(self, secrets_file_path='./.secrets.json'):
        self.secrets_file_path = secrets_file_path

    def get_secrets(self) -> Secrets:
        with open(self.secrets_file_path, 'rb') as f:
            secrets: Secrets = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
            return secrets