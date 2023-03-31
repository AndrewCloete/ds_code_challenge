from service.secrets import SecretsService
from service.s3_client import S3ClientService
from repository.h3 import H3Repository, H3Source
from repository.service_request import ServiceRequestRepository, SRSource
from repository.cache import PoormansLocalFileCache
import compare


REGION = 'af-south-1'
BUCKET_NAME = 'cct-ds-code-challenge-input-data'
CACHE_DIR = './cache'


s3_client_service = S3ClientService(REGION, SecretsService())
repo_cache = PoormansLocalFileCache(CACHE_DIR)
h3_repo = H3Repository(BUCKET_NAME, s3_client_service, repo_cache)
sr_repo = ServiceRequestRepository(BUCKET_NAME, s3_client_service, repo_cache)


# df = sr_repo.get_request_entries(SRSource.UNJOINED)
# print(df.head())

def get_h3():
    df_l8_queried = h3_repo.query_features(H3Source.LEVEL_8_to_10, resolution_level=8)
    df_l8_given = h3_repo.query_features(H3Source.LEVEL_8_ONLY)
    cmp = df_l8_given["index"].compare(df_l8_queried["index"])
    assert cmp.empty

get_h3()



