import json

from secrets_provider import SecretsProvider
from h3_repository import H3Repository
import compare


REGION = 'af-south-1'
BUCKET_NAME = 'cct-ds-code-challenge-input-data'
KEY_RES_8_to_10 = 'city-hex-polygons-8-10.geojson'
KEY_RES_8 = 'city-hex-polygons-8.geojson'


h3_repo = H3Repository(REGION, BUCKET_NAME, SecretsProvider())


l8_queried = h3_repo.query_features(KEY_RES_8_to_10, 8)
l8_given = h3_repo.query_features(KEY_RES_8)


l8_queried_indexes = H3Repository.indexes(l8_queried)
l8_given_indexes = H3Repository.indexes(l8_given)

comparitors = [
    compare.compare_by_list_equality,
    compare.compare_by_set_equality,
    compare.compare_by_hash
]

for comparitor in comparitors:
    comparitor(l8_queried_indexes, l8_given_indexes)



