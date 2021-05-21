import argparse
import logging
import re

import boto3
import botocore


logger = logging.getLogger(__name__)


def parse_s3(s3path):
    """Parse s3 path. Source: https://github.com/MSIA/2021-msia423/blob/main/aws-s3/s3.py
    Args:
        s3path (string) : Input s3's path
    Returns:
        string1,string2 (string,string): name of S3, path of S3 Bucket
    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path, s3path):
    """Upload raw data to S3 bucket.
    Args:
        local_path (string): path to local file to be uploaded
        s3path (string): path to upload on S3 bucket
    Returns:
        None
    """
    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)

