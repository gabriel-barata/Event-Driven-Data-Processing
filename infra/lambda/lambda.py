from datetime import datetime
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import boto3
import os

ldn_bucket = os.environ.get("LANDING_BUCKET")
stg_bucket = os.environ.get("STAGING_BUCKET")

s3 = boto3.client('s3')

def handler(event, context):

    file_names = []

    msg_id = event["Records"]["messageId"]

    for record in event["Records"]:

        message = record["body"]
        file_name = message["object"]["key"]

        s3.download_file(ldn_bucket, file_name, f'/tmp/{file_name}')

        file_names.append(file_name)

    dfs = []

    for file_name in file_names:
        df = pd.read_json(file_name)
        dfs.append(df)

    data = pd.concat(dfs)

    pq.write_table(pq.Table, from_pandas(data), f'/temp/{datetime.today()}-{msg_id}.parquet')
    s3.upload_file(f'/temp/{datetime.today()}-{msg_id}.parquet', stg_bucket, f'{datetime.today()}-{msg_id}.parquet')

    return 0