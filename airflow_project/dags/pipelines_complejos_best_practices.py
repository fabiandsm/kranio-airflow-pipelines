from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import random


# ----------------------------
# Funciones del pipeline
# ----------------------------
def validar_calidad_datos(**context):
    calidad = random.choice(["alta", "media", "baja"])
    context["ti"].xcom_push(key="calidad", value=calidad)
    return calidad


def decidir_procesamiento(**context):
    calidad = context["ti"].xcom_pull(
        task_ids="validar_calidad",
        key="calidad",
    )

    if calidad == "alta":
        return "procesamiento_rapido"
    else:
        return "procesamiento_completo"


def procesamiento_rapido():
    print("Procesamiento rápido ejecutado")
    return "ok"


def procesamiento_completo():
    print("Procesamiento completo ejecutado")
    return "ok"


# ----------------------------
# Definición del DAG
# ----------------------------
with DAG(
    dag_id="pipeline_avanzado_complejo",
    description="Pipeline con patrones avanzados y best practices",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(hours=1),
    },
    tags=["best_practices", "demo", "ci_ready"],
) as dag:

    # Inicio pipeline
    inicio = EmptyOperator(task_id="inicio")

    # Validación de calidad
    validar = PythonOperator(
        task_id="validar_calidad",
        python_callable=validar_calidad_datos,
    )

    # Decisión de ruta
    decidir = BranchPythonOperator(
        task_id="decidir_ruta",
        python_callable=decidir_procesamiento,
    )

    # Ruta rápida
    ruta_rapida = PythonOperator(
        task_id="procesamiento_rapido",
        python_callable=procesamiento_rapido,
    )

    # Ruta completa
    ruta_completa = PythonOperator(
        task_id="procesamiento_completo",
        python_callable=procesamiento_completo,
    )

    # ----------------------------
    # TaskGroup procesamiento pesado
    # ----------------------------
    with TaskGroup("procesamiento_pesado") as procesamiento_group:

        paso1 = EmptyOperator(task_id="paso1")
        paso2 = EmptyOperator(task_id="paso2")
        paso3 = EmptyOperator(task_id="paso3")

        paso1 >> paso2 >> paso3

    # Unión de rutas
    union = EmptyOperator(task_id="union_rutas")

    # Fin pipeline
    fin = EmptyOperator(task_id="fin")

    # ----------------------------
    # Dependencias
    # ----------------------------
    inicio >> validar >> decidir

    decidir >> [
        ruta_rapida,
        ruta_completa,
        procesamiento_group,
    ]

    [ruta_rapida, ruta_completa, procesamiento_group] >> union >> fin
