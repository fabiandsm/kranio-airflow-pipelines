from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.stats import Stats
from datetime import datetime, timedelta
import logging
import time

logger = logging.getLogger(__name__)


def extract_with_metrics(**context):
    start = time.monotonic()
    try:
        # Simulación extracción
        records = 1000
        duration_s = 45.2

        # Métricas
        Stats.gauge("pipeline.extract.records", records)
        Stats.timing("pipeline.extract.duration_ms", int(duration_s * 1000))

        logger.info(
            "Extract completed",
            extra={"records": records, "duration_s": duration_s},
        )

        return {"records": records, "duration_s": duration_s}

    except Exception:
        Stats.incr("pipeline.extract.errors")
        logger.exception("Extract failed")
        raise

    finally:
        real_ms = int((time.monotonic() - start) * 1000)
        Stats.timing("pipeline.extract.real_duration_ms", real_ms)


def transform_with_metrics(**context):
    ti = context["ti"]
    input_data = ti.xcom_pull(task_ids="extract")

    try:
        output_records = int(input_data["records"] * 0.95)
        quality_score = 0.98

        Stats.gauge("pipeline.transform.quality", quality_score)
        Stats.gauge("pipeline.transform.output_records", output_records)

        if quality_score < 0.9:
            logger.warning(
                "Low quality score",
                extra={"quality_score": quality_score},
            )

        return {"output_records": output_records, "quality": quality_score}

    except Exception:
        Stats.incr("pipeline.transform.errors")
        logger.exception("Transform failed")
        raise


def load_with_metrics(**context):
    ti = context["ti"]
    transform_data = ti.xcom_pull(task_ids="transform")

    try:
        records_loaded = transform_data["output_records"]
        load_time_s = 12.5

        Stats.gauge("pipeline.load.records_loaded", records_loaded)
        Stats.timing("pipeline.load.duration_ms", int(load_time_s * 1000))

        throughput = records_loaded / load_time_s
        Stats.gauge("pipeline.load.throughput_rps", throughput)

        return {"loaded": records_loaded, "throughput_rps": throughput}

    except Exception:
        Stats.incr("pipeline.load.errors")
        logger.exception("Load failed")
        raise


def dag_success_callback(context):
    dag_run = context["dag_run"]

    if dag_run.start_date and dag_run.end_date:
        duration_s = (
            dag_run.end_date - dag_run.start_date
        ).total_seconds()

        Stats.timing("pipeline.dag.duration_ms", int(duration_s * 1000))

    Stats.incr("pipeline.dag.success")
    logger.info("DAG completed successfully")


def dag_failure_callback(context):
    Stats.incr("pipeline.dag.failure")
    logger.error(
        "DAG failed",
        extra={"dag_id": context["dag"].dag_id},
    )


def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    Stats.incr("pipeline.sla.violations")
    logger.warning("SLA missed", extra={"dag_id": dag.dag_id})


dag = DAG(
    dag_id="pipeline_monitoring_demo",
    description="Pipeline con métricas y monitoreo completos",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "execution_timeout": timedelta(hours=2),
        "sla": timedelta(hours=1),
    },
    on_success_callback=dag_success_callback,
    on_failure_callback=dag_failure_callback,
    sla_miss_callback=sla_miss_callback,
    tags=["monitoring", "production"],
)

extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract_with_metrics,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform_with_metrics,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load_with_metrics,
    dag=dag,
)

extract_task >> transform_task >> load_task
