from datetime import datetime

from incident_response.runbook import (
    IncidentRunbook,
    configure_logging,
)


def main():
    # Configurar logging
    configure_logging()

    # Crear runbook
    runbook = IncidentRunbook()

    # Contexto del incidente simulado
    incident_context = {
        "triggered_by": "alert_pipeline_down",
        "affected_components": ["etl_pipeline", "data_warehouse"],
        "start_time": datetime.now(),
        "symptoms": [
            "scheduler_not_responding",
            "tasks_queued",
        ],
    }

    # Ejecutar manejo de incidente
    response = runbook.handle_incident(
        "pipeline_down",
        incident_context,
    )

    # Mostrar resultados
    print("\nRespuesta a incidente:")
    print(f"Tipo: {response['incident_type']}")
    print(f"Severidad: {response['severity']}")
    print(f"Resuelto: {response['resolved']}")
    print(f"Duración: {response['duration_seconds']:.2f}s")

    print("\nPasos ejecutados:")
    for step in response["steps_executed"]:
        status = "✅" if step["success"] else "❌"
        print(f"{status} {step['step']}")


if __name__ == "__main__":
    main()