
import boto3
from secrets_provider import SecretsProvider

class H3Repository:
    def __init__(self, region: str, bucket_name: str, secrets_provider: SecretsProvider):
        secrets = secrets_provider.get_secrets()
        session = boto3.session.Session(
            aws_access_key_id=secrets.s3.access_key,
            aws_secret_access_key=secrets.s3.secret_key,
            region_name=region
        )
        self.bucket_name = bucket_name
        self.s3 = session.client('s3')

    def cacheFileInTmp(self, key: str):
        with open(f"/tmp/{key}", 'wb') as f:
            self.s3.download_fileobj(self.bucket_name, key, f)
    
    def queryResolution(self, key: str, resolution: int):

        response = self.s3.select_object_content(
            Bucket=self.bucket_name,
            Key=key,
            Expression=f"SELECT * FROM S3Object[*].features[*] as features  WHERE features.properties.resolution = {resolution}",
            ExpressionType='SQL',
            InputSerialization={'JSON': { 'Type': 'DOCUMENT' }},
            OutputSerialization={'JSON': {}}
            )


        event_stream = response['Payload']
        end_event_received = False
        # Iterate over events in the event stream as they come
        for event in event_stream:
            # If we received a records event, write the data to a file
            if 'Records' in event:
                data = event['Records']['Payload']
                print(data)
            # If we received a progress event, print the details
            elif 'Progress' in event:
                print(event['Progress']['Details'])
            # End event indicates that the request finished successfully
            elif 'End' in event:
                print('Result is complete')
                end_event_received = True
        if not end_event_received:
            raise Exception("End event not received, request incomplete.")