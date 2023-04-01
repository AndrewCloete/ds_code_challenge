from service.secrets import SecretsService
from service.s3_client import S3ClientService
from repository.h3 import H3Repository, H3Source
from repository.service_request import ServiceRequestRepository, SRSource
from repository.cache import PoormansLocalFileCache
from repository.winddata import WindDataRepository
from timer import time_the_thing


REGION = 'af-south-1'
BUCKET_NAME = 'cct-ds-code-challenge-input-data'
CACHE_DIR = './cache'

s3_client_service = S3ClientService(REGION, SecretsService())
repo_cache = PoormansLocalFileCache(CACHE_DIR)
sr_repo = ServiceRequestRepository(BUCKET_NAME, s3_client_service, repo_cache)
h3_repo = H3Repository(BUCKET_NAME, s3_client_service, repo_cache)
winddata_repo = WindDataRepository()

@time_the_thing("get_request_entries")
def test_service_request_repo():
    df = sr_repo.get_request_entries(SRSource.UNJOINED)
    (l, w) = df.shape
    assert(l > 900000)
    assert(w == 16)

@time_the_thing("get_h3")
def test_h3_repo():
    df_l8_queried = h3_repo.query_features(H3Source.LEVEL_8_to_10, resolution_level=8)
    (l, w) = df_l8_queried.shape
    print(f"l8: {l} x {w}")
    assert(l > 3800)
    assert(w == 5)


def test_compare_h3_select():
    df_l8_queried = h3_repo.query_features(H3Source.LEVEL_8_to_10, resolution_level=8)
    df_l8_given = h3_repo.query_features(H3Source.LEVEL_8_ONLY)
    
    @time_the_thing("compare H3 select")
    def compare():
        cmp = df_l8_given["index"].compare(df_l8_queried["index"])
        assert cmp.empty
    compare()


@time_the_thing("get_winddata")
def test_winddata_repo():
    df = winddata_repo.get_as_dataframe()
    (l, w) = df.shape
    assert(l > 8000)
    assert(w == 15)

test_service_request_repo()
test_h3_repo()
test_compare_h3_select()
test_winddata_repo()





