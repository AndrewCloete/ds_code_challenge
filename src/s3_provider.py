
import boto3
from secrets_provider import SecretsProvider

class S3ClientProvider:
    def __init__(self, region: str, secrets_provider: SecretsProvider):
        secrets = secrets_provider.get_secrets()
        session = boto3.session.Session(
            aws_access_key_id=secrets.s3.access_key,
            aws_secret_access_key=secrets.s3.secret_key,
            region_name=region
        )
        self.s3 = session.client('s3')

    def getClient(self):
        return self.s3