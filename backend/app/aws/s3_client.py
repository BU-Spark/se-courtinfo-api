from os.path import join
from pathlib import Path
from typing import Tuple, Optional

import boto3
from botocore.exceptions import ClientError
from botocore.client import Config

from app.core import config

s3_client = None


def get_s3_client() -> boto3.client:
    global s3_client

    if s3_client is None:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=config.S3_KEY_INTERNAL,
            aws_secret_access_key=config.S3_SECRET_INTERNAL,
            config=Config(signature_version='s3v4')

        )
    return s3_client


def upload_file_to_s3(client: boto3.client, file_path: str, obj_prefix: str, bucket: str) -> Tuple[bool, Optional[str]]:
    file_name = join(obj_prefix, Path(file_path).name)
    try:
        client.upload_file(file_path, bucket, file_name)
    except ClientError as e:
        return False, None
    return True, file_name


# Source
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
def create_presigned_url(client: boto3.client, bucket_name, object_name, expiration=config.S3_LINK_TTL):
    """Generate a presigned URL to share an S3 object

    :param client: S3 Client
    :type client: boto3.client
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = client.generate_presigned_url('get_object',
                                                 Params={'Bucket': bucket_name,
                                                         'Key': object_name},
                                                 ExpiresIn=expiration)
    except ClientError as e:
        raise e
    # The response contains the presigned URL
    return response
