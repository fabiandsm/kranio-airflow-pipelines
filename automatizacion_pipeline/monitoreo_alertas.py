from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Any
import logging
import random
import time

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator, get_current_context
from airflow.operators.email import EmailOperator


# =============================================================================
# Logging
# =============================================================================
logger = logging.getLogger("pipeline_monitorado")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# =============================================================================
# Callbacks
# =============================================================================
def on_failure_alert(context: Dict[str, Any]) -> None:
    ti = context["task_instance"]
    dag_id = context["dag"].dag_id
    run_id = context.get("run_id")
    error = context.get("exception")

    logger.error(
        f"""
🚨 ALERTA DE FALLO 🚨
DAG: {dag_id}
Task: {ti.task_id}
Run ID: {run_id}
Error: {error}
Log: {ti.log_url}
"""
    )


def on_success_summary(context: Dict[str, Any]) -> None:
    dag_run = context.get("dag_run")
    if dag_run and dag_run.start_date and dag_run.end_date:
        duration = (dag_run.end_date - dag_run.start_date).total_seconds()
        logger.info(
            f"DAG {dag_run.dag_id} completado en {duration:.1f} segundos"
        )


def sla_miss_callback(context: Dict[str, Any], **kwargs) -> None:
    logger.warning(
        f"SLA MISS | DAG={context['dag'].dag_id} | TASK={context['task'].task_id}"
    )


# =============================================================================
# Tasks
# =============================================================================
def procesar_datos_con_metricas() -> Dict[str, Any]:
    context = get_current_context()
    ti = context["ti"]

    logger.info("Iniciando procesamiento de datos")

    processing_time = random.uniform(10, 60)
    time.sleep(processing_time)

    resultado = {
        "registros_procesados": random.randint(1000, 5000),
        "tiempo_procesamiento_s": processing_time,
        "tasa_exito": random.uniform(0.95, 1.0),
        "timestamp_utc": datetime.utcnow().isoformat(),
    }

    ti.xcom_push(key="metricas", value=resultado)
    logger.info(f"Métricas generadas: {resultado}")

    return resultado


def validar_metricas() -> bool:
    context = get_current_context()
    ti = context["ti"]

    metricas = ti.xcom_pull(task_ids="procesar_datos", key="metricas")

    if not metricas:
        raise AirflowException("No se encontraron métricas en XCom")

    if metricas["tasa_exito"] < 0.90:
        raise AirflowException(
            f"Tasa de éxito baja: {metricas['tasa_exito']:.2%}"
        )

    if metricas["tiempo_procesamiento_s"] > 300:
        logger.warning(
            f"Tiempo de procesamiento alto: {metricas['tiempo_procesamiento_s']:.1f}s"
        )

    logger.info("Validación de métricas exitosa")
    return True


def verificar_sla_post() -> float:
    context = get_current_context()
    dag_run = context.get("dag_run")

    if not dag_run or not dag_run.start_date:
        return -1.0

    duration = (
        datetime.utcnow() - dag_run.start_date.replace(tzinfo=None)
    ).total_seconds()

    sla_seconds = 7200  # 2 horas

    if duration > sla_seconds:
        logger.warning(f"SLA violado: {duration:.1f}s > {sla_seconds}s")
    else:
        logger.info(f"SLA OK: {duration:.1f}s")

    return duration


# =============================================================================
# DAG
# =============================================================================
default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
    "on_failure_callback": on_failure_alert,
}

with DAG(
    dag_id="pipeline_monitorado",
    description="Pipeline con monitoreo, métricas y alertas por email",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["monitoring", "email"],
) as dag:

    procesar = PythonOperator(
        task_id="procesar_datos",
        python_callable=procesar_datos_con_metricas,
    )

    validar = PythonOperator(
        task_id="validar_metricas",
        python_callable=validar_metricas,
    )

    notificar_exito = EmailOperator(
        task_id="notificar_exito",
        to=["airflow.alerts333@gmail.com"],
        subject="Pipeline ETL Completado - {{ ds }}",
        html_content="""
        <h2>✅ Pipeline ETL Completado Exitosamente</h2>
        <p><b>Fecha:</b> {{ ds }}</p>
        <p><b>Run ID:</b> {{ run_id }}</p>
        <p><b>Inicio:</b> {{ dag_run.start_date }}</p>
        <p><b>Fin:</b> {{ dag_run.end_date }}</p>
        """,
        trigger_rule="all_success",
        retries=0,
    )

    verificar = PythonOperator(
        task_id="verificar_sla",
        python_callable=verificar_sla_post,
        trigger_rule="all_done",
    )

    procesar >> validar >> notificar_exito >> verificar
