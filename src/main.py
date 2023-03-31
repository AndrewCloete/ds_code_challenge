from service.secrets import SecretsService
from service.s3_client import S3ClientService
from repository.h3 import H3Repository, H3Source
from repository.service_request import ServiceRequestRepository, SRSource
import compare


REGION = 'af-south-1'
BUCKET_NAME = 'cct-ds-code-challenge-input-data'
H3_CACHE_DIR = './cache/h3'
SR_CACHE_DIR = './cache/sr'


s3_client_service = S3ClientService(REGION, SecretsService())
h3_repo = H3Repository(BUCKET_NAME, s3_client_service, H3_CACHE_DIR)
sr_repo = ServiceRequestRepository(BUCKET_NAME, s3_client_service, SR_CACHE_DIR)


# df = sr_repo.get_request_entries(SRSource.UNJOINED)
# print(df.head())

def get_h3():
    df_l8_queried = h3_repo.query_features(H3Source.LEVEL_8_to_10, resolution_level=8)
    df_l8_given = h3_repo.query_features(H3Source.LEVEL_8_ONLY)
    cmp = df_l8_given["index"].compare(df_l8_queried["index"])
    assert cmp.empty

get_h3()



