import pytest
from airflow.models import DagBag
from pathlib import Path

DAG_ID = "pipeline_avanzado_complejo"


@pytest.fixture(scope="session")
def dagbag():
    dags_path = Path(__file__).parents[2] / "dags"
    return DagBag(dag_folder=str(dags_path), include_examples=False)


def test_dag_cargado(dagbag):
    dag = dagbag.get_dag(DAG_ID)
    assert dag is not None
    assert len(dag.tasks) >= 5


def test_tarea_inicio(dagbag):
    dag = dagbag.get_dag(DAG_ID)
    inicio = dag.get_task("inicio")
    assert not inicio.upstream_task_ids


def test_tarea_fin(dagbag):
    dag = dagbag.get_dag(DAG_ID)
    fin = dag.get_task("fin")
    assert not fin.downstream_task_ids


def test_taskgroup_existe(dagbag):
    dag = dagbag.get_dag(DAG_ID)
    assert "procesamiento_pesado.paso1" in dag.task_ids


def test_branching_calidad_alta():
    from airflow_project.dags.pipelines_complejos_best_practices import (
        decidir_procesamiento,
    )

    class DummyTI:
        def xcom_pull(self, **kwargs):
            return "alta"

    result = decidir_procesamiento(context={"ti": DummyTI()})
    assert result == "procesamiento_rapido"