from enum import Enum
import gzip


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

    def get_request_entries(self, source: SRSource):
        cache_result = self.cache.get(source.name)
        if cache_result is not None:
            return cache_result.decode('utf-8').splitlines()

        response = self.s3.get_object(Bucket=self.bucket_name, Key=source.value)
        uncompressed = gzip.decompress(response["Body"].read())
        self.cache.put(source.name, uncompressed)
        return uncompressed.decode('utf-8').splitlines()


    