from enum import Enum
import gzip

import pandas as pd


from service.s3_client import S3ClientService
from repository.cache import PoormansLocalFileCache

class SRSource(Enum):
    UNJOINED = 'sr.csv.gz'
    JOINED = 'sr_hex.csv.gz'

class ServiceRequestRepository:
    def __init__(self, bucket_name: str, s3_client_provider: S3ClientService, cache: PoormansLocalFileCache):
        self.bucket_name = bucket_name
        self.s3 = s3_client_provider.get_client()
        self.cache = cache 

    def __cache_name(self, source: SRSource):
        return f"{source.name}.csv"

    def __cache_file_path_handler(cache_path: str):
        return pd.read_csv(cache_path)

    def get_request_entries(self, source: SRSource) -> pd.DataFrame:
        cache_name = self.__cache_name(source)
        cache_result = self.cache.get(cache_name, ServiceRequestRepository.__cache_file_path_handler)
        if cache_result is not None:
            print("Using cached", cache_name)
            return cache_result 
        print("Cache miss for", cache_name)

        response = self.s3.get_object(Bucket=self.bucket_name, Key=source.value)
        uncompressed = gzip.decompress(response["Body"].read())
        self.cache.put(cache_name, uncompressed)
        return self.cache.get(cache_name, ServiceRequestRepository.__cache_file_path_handler)
    


    