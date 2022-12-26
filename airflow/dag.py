
import os
import sys

sys.path.append('C:\\Users\\Andrew\\repos\\new-york-times-data-pipeline\\src')

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import extract_from_api
import load_to_gcp
import config

# print(config.directory)

# os.chdir(src.config.directory)

schedule_interval = '@daily'
start_date = days_ago(1)

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'retries' : 1,
}

with DAG(
    dag_id = 'new_york_times_data_pipeline',
    description = 'nyt_api_ETL_pipeline',
    schedule_interval = schedule_interval,
    default_args = default_args,
    start_date = start_date,
    max_active_runs = 1,
    tags = ['NYT_ETL'],
) as dag:

    extract_nyt_data = PythonOperator(
        task_id = 'extract_nyt_data',
        python_callable = extract_from_api.main,
        dag = dag,
    )

    load_nyt_data = PythonOperator(
        task_id = 'load_nyt_data',
        python_callable = load_to_gcp.main,
        dag = dag,
    )

extract_nyt_data >> load_nyt_data
