import os

import pandas as pd
from datetime import datetime


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime',
               'tpep_dropoff_datetime']
    df_input = pd.DataFrame(data, columns=columns)

    options = {
        'client_kwargs': {
            'endpoint_url': 'http://127.0.0.1:4566'
        }
    }

    input_file = "s3://integration-test-bucket/input_file.parquet"

    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )


# prepare_data()

os.environ["INPUT_FILE_PATTERN"] = "s3://integration-test-bucket/input_file.parquet"
os.environ["OUTPUT_FILE_PATTERN"] = "s3://integration-test-bucket/output_file.parquet"
os.environ["S3_ENDPOINT_URL"] = 'http://127.0.0.1:4566'

os.system("python batch.py 2023 05")

