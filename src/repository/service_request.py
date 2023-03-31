from enum import Enum
import gzip
from io import StringIO

import pandas as pd


from service.s3_client import S3ClientService
from repository.cache import PoormansLocalFileCache

class SRSource(Enum):
    UNJOINED = 'sr.csv.gz'
    JOINED = 'sr_hex.csv.gz'

class ServiceRequestRepository:
    def __init__(self, bucket_name: str, s3_client_provider: S3ClientService, cache_dir: str = None):
        self.bucket_name = bucket_name
        self.s3 = s3_client_provider.get_client()
        self.cache = PoormansLocalFileCache(cache_dir)

    def __cache_name(self, source: SRSource):
        return f"{source.name}.csv"

    def __as_dataframe(bytes_data: bytes) -> pd.DataFrame:
        return pd.read_csv(StringIO(bytes_data.decode('utf-8')))

    def get_request_entries(self, source: SRSource) -> pd.DataFrame:
        cache_result = self.cache.get(self.__cache_name(source))
        if cache_result is not None:
            return ServiceRequestRepository.__as_dataframe(cache_result)

        response = self.s3.get_object(Bucket=self.bucket_name, Key=source.value)
        uncompressed = gzip.decompress(response["Body"].read())
        self.cache.put(self.__cache_name(source), uncompressed)
        return ServiceRequestRepository.__as_dataframe(cache_result)
    


    