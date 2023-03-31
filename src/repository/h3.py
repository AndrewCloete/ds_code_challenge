"""
References:
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_SelectObjectContent.html#API_SelectObjectContent_RequestSyntax
- https://botocore.amazonaws.com/v1/documentation/api/latest/reference/eventstream.html
"""

import json
from typing import Optional, List
from enum import Enum

import geopandas as gpd

from service.s3_client import S3ClientService
from repository.cache import PoormansLocalFileCache

class H3Source(Enum):
    LEVEL_8_to_10 = 'city-hex-polygons-8-10.geojson'
    LEVEL_8_ONLY = 'city-hex-polygons-8.geojson'


class H3Repository:
    def __init__(self, bucket_name: str, s3_client_provider: S3ClientService, cache_dir: str = None):
        self.bucket_name = bucket_name
        self.s3 = s3_client_provider.get_client()
        self.cache = PoormansLocalFileCache(cache_dir)

    def __cache_name(self, source: H3Source, resolution_level: int = None):
        return f"{source.name}_lvl{resolution_level}.geojson"

    def __cache_file_path_handler(cache_path: str):
        return gpd.read_file(cache_path, driver="GeoJSON")

    def query_features(self, source: H3Source, resolution_level: int = None) -> gpd.GeoDataFrame:

        cache_name = self.__cache_name(source, resolution_level)
        cache_result = self.cache.get(cache_name, H3Repository.__cache_file_path_handler)
        if cache_result is not None:
            cache_result

        def build_expression(resolution_level: int = None):
            where_clause = "" if resolution_level is None else f"WHERE feature.properties.resolution = {resolution_level}"
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
            Would typically not raise an exception here and rather return an
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
            Key=source.value,
            Expression=build_expression(resolution_level),
            ExpressionType='SQL',
            InputSerialization={'JSON': { 'Type': 'DOCUMENT' }},
            OutputSerialization={'JSON': { }}
            )

        results = parse_query_response(read_query_event_stream(response['Payload']))

        if results is not None:
            self.cache.put(cache_name, json.dumps({"type": "FeatureCollection", "features": results}).encode('utf-8'))
        
        return self.cache.get(cache_name, H3Repository.__cache_file_path_handler)
        
        
