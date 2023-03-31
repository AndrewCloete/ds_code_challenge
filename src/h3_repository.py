"""
References:
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_SelectObjectContent.html#API_SelectObjectContent_RequestSyntax
- https://botocore.amazonaws.com/v1/documentation/api/latest/reference/eventstream.html
"""

import json
from typing import Optional, List

from s3_provider import S3ClientProvider

class H3Repository:
    def __init__(self, bucket_name: str, s3_client_provider: S3ClientProvider):
        self.bucket_name = bucket_name
        self.s3 = s3_client_provider.getClient()

    def feature_to_index(feature) -> str:
        return feature['properties']['index']

    def indexes(features: List[dict]) -> List[str]:
        return [H3Repository.feature_to_index(feature) for feature in features]

    def query_features(self, key: str, resolution: int = None):

        def build_expression(resolution: int = None):
            where_clause = "" if resolution is None else f"WHERE feature.properties.resolution = {resolution}"
            return f"""SELECT feature FROM S3Object[*].features[*] as feature {where_clause}"""
            
        def read_query_event_stream(event_stream) -> bytes:
            data = b''
            end_event_received = False
            for event in event_stream:
                if 'Records' in event:
                    data += event['Records']['Payload']
                if 'End' in event:
                    end_event_received = True

            """
            Would typically not raise an exception here, but rather return an
            Optional type to allow the caller to handle the error. But this is
            totally sufficient for this exercise.
            """
            if not end_event_received:
                raise Exception("End event not received. Go have some tea")

            return data
            
        def parse_query_response(stream_data: bytes) -> Optional[list]:
            return  [json.loads(line)["feature"] for line in stream_data.split()]

        response = self.s3.select_object_content(
            Bucket=self.bucket_name,
            Key=key,
            Expression=build_expression(resolution),
            ExpressionType='SQL',
            InputSerialization={'JSON': { 'Type': 'DOCUMENT' }},
            OutputSerialization={'JSON': { }}
            )

        return parse_query_response(read_query_event_stream(response['Payload']))
        
        
