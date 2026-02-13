from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import random


# ----------------------------
# Funciones
# ----------------------------
def validar_calidad_datos(**context):
    """Simular validación de calidad"""
    calidad = random.choice(['alta', 'media', 'baja'])
    context['task_instance'].xcom_push(key='calidad', value=calidad)
    return calidad


def decidir_procesamiento(**context):
    """Decidir ruta basado en calidad"""
    calidad = context['task_instance'].xcom_pull(
        task_ids='validar_calidad',
        key='calidad'
    )

    if calidad == 'alta':
        return 'procesamiento_rapido'
    else:
        return 'procesamiento_completo'


def procesamiento_rapido():
    print("Procesamiento optimizado para datos de alta calidad")
    return "Procesado rápido"


def procesamiento_completo():
    print("Procesamiento completo con validaciones adicionales")
    return "Procesado completo"


# ----------------------------
# DAG
# ----------------------------
dag = DAG(
    'pipeline_avanzado_complejo',
    description='Pipeline con patrones avanzados y best practices',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
        'execution_timeout': timedelta(hours=1)
    }
)


# ----------------------------
# Tasks base
# ----------------------------
inicio = DummyOperator(task_id='inicio', dag=dag)

validar = PythonOperator(
    task_id='validar_calidad',
    python_callable=validar_calidad_datos,
    dag=dag
)

decidir = BranchPythonOperator(
    task_id='decidir_ruta',
    python_callable=decidir_procesamiento,
    dag=dag
)

ruta_rapida = PythonOperator(
    task_id='procesamiento_rapido',
    python_callable=procesamiento_rapido,
    dag=dag
)

ruta_completa = PythonOperator(
    task_id='procesamiento_completo',
    python_callable=procesamiento_completo,
    dag=dag
)


# ----------------------------
# TaskGroup CORREGIDO
# ----------------------------
with TaskGroup('procesamiento_pesado', dag=dag) as procesamiento_group:

    paso1 = DummyOperator(task_id='paso1', dag=dag)
    paso2 = DummyOperator(task_id='paso2', dag=dag)
    paso3 = DummyOperator(task_id='paso3', dag=dag)

    # relaciones internas
    paso1 >> paso2 >> paso3


# ----------------------------
# Unión y final
# ----------------------------
union = DummyOperator(task_id='union_rutas', dag=dag)
fin = DummyOperator(task_id='fin', dag=dag)


# ----------------------------
# Dependencias
# ----------------------------
inicio >> validar >> decidir

decidir >> [ruta_rapida, ruta_completa, procesamiento_group]

[ruta_rapida, ruta_completa, procesamiento_group] >> union >> fin
