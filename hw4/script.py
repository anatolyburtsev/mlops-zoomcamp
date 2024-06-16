#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pickle
import pandas as pd
import numpy as np
import requests
from io import BytesIO
import click

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']


def read_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    file_content = BytesIO(response.content)

    df = pd.read_parquet(file_content)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df['duration'].dt.total_seconds() / 60

    df = df[(df['duration'] >= 1) & (df['duration'] <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype(int).astype(str)

    return df


@click.command()
@click.option('--year', type=int, help='Year as a four-digit number')
@click.option('--month', type=int, help='Month as a number (1-12)')
def process_taxi_data(year, month):
    month_str = str(month).zfill(2)
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month_str}.parquet')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    click.echo(f"str = {np.mean(y_pred)}")


if __name__ == '__main__':
    process_taxi_data()
