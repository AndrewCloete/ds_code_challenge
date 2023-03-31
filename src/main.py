"""
References:
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/select_object_content.html
- https://docs.aws.amazon.com/AmazonS3/latest/API/API_SelectObjectContent.html#API_SelectObjectContent_RequestSyntax
- https://botocore.amazonaws.com/v1/documentation/api/latest/reference/eventstream.html
"""

from secrets_provider import SecretsProvider
from h3_repository import H3Repository

REGION = 'af-south-1'
BUCKET_NAME = 'cct-ds-code-challenge-input-data'
KEY = 'city-hex-polygons-8-10.geojson'


h3_repo = H3Repository(REGION, BUCKET_NAME, SecretsProvider())

h3_repo.queryResolution(KEY, 8)


