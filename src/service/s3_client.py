
import boto3
from service.secrets import SecretsService

class S3ClientService:
    def __init__(self, region: str, secrets_provider: SecretsService):
        secrets = secrets_provider.get_secrets()
        session = boto3.session.Session(
            aws_access_key_id=secrets.s3.access_key,
            aws_secret_access_key=secrets.s3.secret_key,
            region_name=region
        )
        self.s3 = session.client('s3')

    def get_client(self):
        return self.s3