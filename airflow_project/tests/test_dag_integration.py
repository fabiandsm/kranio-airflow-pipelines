class TestDAGIntegration:

    def test_dag_runs_without_errors(self, dagbag):
        dag = dagbag.get_dag('etl_pipeline')

        # Lanza excepción si hay ciclos
        dag.test_cycle()

        for task in dag.tasks:
            for upstream in task.upstream_list:
                assert upstream in dag.tasks
