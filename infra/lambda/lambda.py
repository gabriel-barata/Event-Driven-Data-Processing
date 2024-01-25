import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import boto3

from datetime import datetime
import json
import os


ldn_bucket = os.environ.get("LANDING_BUCKET")
stg_bucket = os.environ.get("STAGING_BUCKET")

s3 = boto3.client('s3')


def handler(event, context):

    event = json.loads(event)

    file_names = []
    msg_id = event["Records"][0]["messageId"]

    for record in event["Records"]:
        message = record["body"]["Message"]["detail"]
        file_name = message["object"]["key"]

        s3.download_file(ldn_bucket, file_name, f'/tmp/{file_name}')
        file_names.append(file_name)

    data = []
    for file_name in file_names:
        with open(f'/tmp/{file_name}', 'r') as file:
            json_data = json.load(file)
            data.extend(json_data)

    table = pa.Table.from_pandas(
        pd.raed_json(data))

    pq.write_table(table, f'/temp/{datetime.today()}-{msg_id}.parquet')
    s3.upload_file(
        f'/temp/{datetime.today()}-{msg_id}.parquet',
        stg_bucket, f'{datetime.today()}-{msg_id}.parquet'
    )

    return 0
