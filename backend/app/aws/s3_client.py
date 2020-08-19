from os.path import join
from pathlib import Path
from typing import Tuple, Optional

import boto3
from botocore.exceptions import ClientError

from app.core import config


def upload_file_to_s3(file_path: str, obj_prefix: str, bucket: str) -> Tuple[bool, Optional[str]]:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config.S3_KEY_INTERNAL,
        aws_secret_access_key=config.S3_SECRET_INTERNAL
    )
    file_name = join(obj_prefix, Path(file_path).name)
    try:
        s3_client.upload_file(file_path, bucket, file_name)
    except ClientError as e:
        return False, None
    return True, file_name
