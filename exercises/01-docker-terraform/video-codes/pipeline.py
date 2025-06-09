#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    # loading the parameters
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    # downloading the file
    os.system(f"wget {url} -O {csv_name}")
    # creating the connection to pgsql db
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # reading the huge CSV file in chunks
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    # loading the first chunk
    df = next(df_iter)
    # parsing date and time columns
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    # pushing the data into the database
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    while True: 
        try:
            # getting the start time
            t_start = time()
            # loading the next chunk
            df = next(df_iter)
            # parsing date and time columns
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            # pushing the data into the database
            df.to_sql(name=table_name, con=engine, if_exists='append')
            # getting the finish time
            t_end = time()
            # TODO: logging for now to console, but better to install a logger and log there.
            print('inserted another chunk, took %.3f second' % (t_end - t_start))
        except StopIteration:
            # TODO: logging for now to console, but better to install a logger and log there.
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    #
    args = parser.parse_args()
    #
    print(args)
    main(args)
