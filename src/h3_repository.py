"""
References:
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_SelectObjectContent.html#API_SelectObjectContent_RequestSyntax
- https://botocore.amazonaws.com/v1/documentation/api/latest/reference/eventstream.html
"""

import json

import boto3
from secrets_provider import SecretsProvider
from typing import TypedDict, Optional, List


class ReadStreamResponse(TypedDict):
    data: bytes
    details: list
    end_event_received: bool

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

    def query_features(self, key: str, resolution: int = None):

        def build_expression(resolution: int = None):
            where_clause = "" if resolution is None else f"WHERE feature.properties.resolution = {resolution}"
            return f"""SELECT feature FROM S3Object[*].features[*] as feature {where_clause}"""
            
        def read_query_event_stream(event_stream) -> ReadStreamResponse:
            data = b''
            details = []
            end_event_received = False
            for event in event_stream:
                if 'Records' in event:
                    data += event['Records']['Payload']
                # if 'Progress' in event:
                #     details.append(event['Progress']['Details'])
                if 'End' in event:
                    end_event_received = True
            
            return {"data": data, "details":details, "end_event_received": end_event_received}
            
        def parse_query_response(response) -> Optional[list]:
            if not response["end_event_received"]:
                return None 
            
            return  [json.loads(line)["feature"] for line in response["data"].split()]

        response = self.s3.select_object_content(
            Bucket=self.bucket_name,
            Key=key,
            Expression=build_expression(resolution),
            ExpressionType='SQL',
            InputSerialization={'JSON': { 'Type': 'DOCUMENT' }},
            OutputSerialization={'JSON': { }}
            )

        streamResult = read_query_event_stream(response['Payload'])
        return parse_query_response(streamResult)
        
        
