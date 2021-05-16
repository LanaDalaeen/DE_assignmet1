import datetime as dt
from datetime import timedelta
from airflow.operators.python_operators import PythonOperator
from sqlalchemy import create_engine
import psycopg2
from faker import Faker
import csv
import pandas as pd 
from pymongo import MongoClient
import json

host="postgres" # use "localhost" if you access from outside the localnet docker-compose env 
database="testDB"
user="me"
password="1234"
port='5432'
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

client = MongoClient('mongo:27017', 
                        username='root',
                         password='example')

def step_1():
 output=open('data.csv','w')
 fake=Faker()
 header=['name','age','street','city','state','zip','lng','lat']
 mywriter=csv.writer(output)
 mywriter.writerow(header)
 for r in range(1000000):
    row =[fake.name(),fake.random_int(min=18,max=80, step=1), 
                       fake.street_address(), fake.city(),fake.state(),
                       fake.zipcode(),fake.longitude(),fake.latitude()]
    mywriter.writerow(row)
 output.close()
 DF.to_sql('users2020', engine, if_exists='replace',index=False)

def step_2():
    df = pd.read_csv('data.csv')
    df.to_json('data.json', orient='records')
def step_3():
    db = client['de_assignment_1']
    articles = db.random
    f = open('data.json',)
    data = json.load(f)
    result = articles.insert_many(data)

default_args = { 'owner' :'lana',
                  'start_date': dt.datetime(2021,5,16),
                  'retries':1,
                  'retry_delay': dt.timedelta(minutes=5)}

dag=DAG(dag_id='dag', default_args=default_args)
step_1_task= PythonOperator(task_id='step1', python_collable=step_1, dag=dag)
step_2_task= PythonOperator(task_id='step2', python_collable=step_2, dag=dag)
step_3_task= PythonOperator(task_id='step3', python_collable=step_3, dag=dag)
step_1_task>>step_2_task>>step_3_task

