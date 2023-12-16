from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from main2 import arguments


default_args = {
   'owner':  'airflow',
   'depends_on_past': False,
   'start_date': datetime(2023, 11, 22),
   'email': ['i202435@gmail.com'],
   'email_on_failure': False,
   'email_on_retry': False,
   'retries': 1,
   'retry_delay': timedelta(minutes=1) }
   
dag = DAG(
   'Islamic_prayer_DAG',
   default_args=default_args,
   description='Airflow ETL Code for scrapping prayer time data'
)

run_etl = PythonOperator(
   task_id='ETL_AIRFLOW_DAG',
   python_callable= arguments,
   dag=dag
)

run_etl

