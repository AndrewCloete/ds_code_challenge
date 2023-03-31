from enum import Enum
import gzip
from pathlib import Path


from service.s3_client import S3ClientService

class SRSource(Enum):
    UNJOINED = 'sr.csv.gz'
    JOINED = 'sr_hex.csv.gz'


class __LocalFileCache:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        if cache_dir is not None:
            Path(cache_dir).mkdir(parents=True, exist_ok=True)

    def __cache_path(self, source: SRSource):
        if self.cache_dir is None:
            return None
        return f"{self.cache_dir}/{source.name}.csv"

    def get(self, source: SRSource):
        if self.cache_dir is None:
            return None
        cache_path = self.__cache_path(source)
        if not Path(cache_path).is_file():
            return None
        with open(cache_path, "rb") as f:
            return f.read()

    def put(self, source: SRSource, data: str):
        if self.cache_dir is None:
            return
        cache_path = self.__cache_path(source)
        with open(cache_path, "wb") as f:
            f.write(data)


class ServiceRequestRepository:
    def __init__(self, bucket_name: str, s3_client_provider: S3ClientService, cache_dir: str = None):
        self.bucket_name = bucket_name
        self.s3 = s3_client_provider.get_client()
        self.cache = __LocalFileCache(cache_dir)

    def get_request_entries(self, source: SRSource):
        cache_result = self.cache.get(source)
        if cache_result is not None:
            return cache_result.decode('utf-8').splitlines()

        response = self.s3.get_object(Bucket=self.bucket_name, Key=source.value)
        uncompressed = gzip.decompress(response["Body"].read())
        self.cache.put(source, uncompressed)
        return uncompressed.decode('utf-8').splitlines()


    