from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import datetime, timedelta
import subprocess
import os

AIRFLOW_PROJECT_PATH = os.path.expanduser('~/airflow_project/new_venv')
INSERT = os.path.join(AIRFLOW_PROJECT_PATH, 'insert.py')
RECOD = os.path.join(AIRFLOW_PROJECT_PATH, 'ocr.py')
READ_OCR_SCRIPT = os.path.join(AIRFLOW_PROJECT_PATH, 'read_ocr.py')
READ_CV_SCRIPT = os.path.join(AIRFLOW_PROJECT_PATH, 'read_cv.py')
PREP = os.path.join(AIRFLOW_PROJECT_PATH, 'prep.py')
LOAD = os.path.join(AIRFLOW_PROJECT_PATH, 'load.py')

def run_insert():
    result = subprocess.run(['python', INSERT], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"insert.py failed with error: {result.stderr}")
    
def run_recodnition():
    result = subprocess.run(['python', RECOD], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"insert.py failed with error: {result.stderr}")
    
def run_read_ocr():
    result = subprocess.run(['python', READ_OCR_SCRIPT], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"read_ocr.py failed with error: {result.stderr}")
   
def run_read_cv():
    result = subprocess.run(['python', READ_CV_SCRIPT], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"read_cv.py failed with error: {result.stderr}")    
   
def run_prep():
    result = subprocess.run(['python', PREP], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"prep.py failed with error: {result.stderr}")
   
def run_load():
    result = subprocess.run(['python', LOAD], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"load.py failed with error: {result.stderr}")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'reader',
    default_args=default_args,
    description='Extract from Archive',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

t1 = PythonOperator(
    task_id='run_insert_script',
    python_callable=run_insert,
    dag=dag,
)

t2 = PythonOperator(
    task_id='run_read_cv',
    python_callable=run_read_cv,
    dag=dag,
)

t3 = PythonOperator(
    task_id='run_OCR',
    python_callable=run_recodnition,
    dag=dag,
)

t4 = PythonOperator(
    task_id='run_read_ocr',
    python_callable=run_read_ocr,
    dag=dag,
)

t5 = PythonOperator(
    task_id='run_prep',
    python_callable=run_prep,
    dag=dag,
)

t6 = PythonOperator(
    task_id='run_load',
    python_callable=run_load,
    dag=dag,
)

t1 >> t2 >> t3 >> t4 >> t5 >> t6