import json
from secrets_provider import SecretsProvider
from h3_repository import H3Repository

REGION = 'af-south-1'
BUCKET_NAME = 'cct-ds-code-challenge-input-data'
KEY_RES_8_to_10 = 'city-hex-polygons-8-10.geojson'
KEY_RES_8 = 'city-hex-polygons-8.geojson'


h3_repo = H3Repository(REGION, BUCKET_NAME, SecretsProvider())

from_all = h3_repo.query_features(KEY_RES_8_to_10, 8)


subset = h3_repo.query_features(KEY_RES_8)
print (json.dumps(subset, indent=2))

print(len(from_all))
print(len(subset))

