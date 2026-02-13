from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

def saludar():
    print("Hola desde Airflow")
    return "OK"

with DAG(
    dag_id="saludo_diario",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    bash = BashOperator(
        task_id="tarea_bash",
        bash_command="echo Hola Airflow"
    )

    python = PythonOperator(
        task_id="tarea_python",
        python_callable=saludar
    )

    bash >> python
