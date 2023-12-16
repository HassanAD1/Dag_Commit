import requests
from datetime import datetime, timedelta
from airflow import models
from google.cloud import bigquery
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import sqlite3
import json
import os


'''with models.DAG(
	dag_id='ETL-PIPELINE',
	schedule="0 04 * * *",
	start_date = datetime.today() - timedelta(days=1),
	catchup=False,
	tags=["LIVE"],
	) as dag:'''

def extract(date="25 March 2021"):
	date="25 March 2021"

    latitude = 33.738045  # Replace this with your current latitude.
    longitude = 73.084488  # Replace this with your current longitude.
    day = 10
    
    api_key = 'http://api.aladhan.com/v1/calendarByAddress/:year/:month'

	url = f'https://api.aladhan.com/v1/calendar/{date}?latitude={latitude}&longitude={longitude}'


	response = requests.get(url)#, headers=headers)
	if response.status_code == 200:
		data = response.json()
		prayer_times = data['data'][day]['timings']
		
		prayer_times.to_csv('prayer_times.csv')
		return prayer_times
	else:
		print(f"Error fetching prayer times: {response.status_code} - {response.text}")
		return None
	
def transform(df):
	df = pd.DataFrame(prayer_times,index=[1,2,3,4,5])
	return df
	
def load(df):
	# Connect to SQLite database
	conn = sqlite3.connect('your_database_name.db')

	# Use to_sql to store in SQLite
	df.to_sql('your_table_name', conn, index=False, if_exists='replace')

	# Close the connection
	conn.close()	

def arguments():

	extract = extract()
	transform = transform(extract)
	load(transform)
	return "table is uploaded successfully"
