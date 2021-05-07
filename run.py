import argparse

import logging.config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('steam-pipeline')

from src.s3 import upload_file_to_s3
from src.create_db import create_db

if __name__ == '__main__':
    """This if statement will parse input arguments of run.py to determine:
        1. Whether you want to upload to s3 bucket or create database 
        2. Whether you want to create local database or create database on RDS
    """
    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Upload to S3/Create DataBase")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for uploading files to s3
    sb_s3 = subparsers.add_parser("upload", description="Upload files to s3")
    sb_s3.add_argument('--s3path', default="s3://2021-msia423-jiang-junpeng/raw/newdata.csv", action="store",
                        help="If used, will load data via pandas")
    sb_s3.add_argument('--local_path', default="data/steamdata/steam.csv", action="store",
                        help="Where to load data to in S3")

    sb_create_db = subparsers.add_parser("create_db", description="Create tables in database")
    sb_create_db.add_argument("--engine_string", default=None,
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'upload':
        upload_file_to_s3(args.local_path, args.s3path)
    elif sp_used == 'create_db':
        create_db(args.engine_string)
    else:
        parser.print_help()
