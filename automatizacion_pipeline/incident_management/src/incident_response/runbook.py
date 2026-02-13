from __future__ import annotations

from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("incident_response")


class IncidentRunbook:
    """Runbook automatizado para respuesta a incidentes"""

    def __init__(self):
        self.incident_types = self._define_incident_types()
        self.escalation_matrix = self._define_escalation()

    # ------------------------------------------------------------------
    # Definición de incidentes
    # ------------------------------------------------------------------
    def _define_incident_types(self) -> Dict[str, Dict[str, Any]]:
        return {
            "pipeline_down": {
                "severity": "CRITICAL",
                "auto_response": True,
                "timeout": timedelta(minutes=15),
                "steps": [
                    "check_airflow_scheduler",
                    "check_database_connectivity",
                    "restart_failed_services",
                    "verify_pipeline_recovery",
                ],
            },
            "data_quality_degraded": {
                "severity": "HIGH",
                "auto_response": False,
                "timeout": timedelta(hours=1),
                "steps": [
                    "isolate_affected_data",
                    "check_upstream_sources",
                    "implement_data_filters",
                    "notify_data_consumers",
                ],
            },
            "performance_degraded": {
                "severity": "MEDIUM",
                "auto_response": True,
                "timeout": timedelta(hours=2),
                "steps": [
                    "check_resource_usage",
                    "scale_resources_if_needed",
                    "optimize_running_queries",
                    "monitor_recovery",
                ],
            },
        }

    # ------------------------------------------------------------------
    # Escalamiento
    # ------------------------------------------------------------------
    def _define_escalation(self) -> Dict[str, Dict[str, str]]:
        return {
            "CRITICAL": {
                "5min": "alert_lead_engineer",
                "15min": "alert_engineering_manager",
                "30min": "alert_vp_engineering",
            },
            "HIGH": {
                "15min": "alert_lead_engineer",
                "45min": "alert_engineering_manager",
            },
            "MEDIUM": {
                "30min": "alert_lead_engineer",
                "2h": "alert_engineering_manager",
            },
        }

    # ------------------------------------------------------------------
    # Manejo principal de incidente
    # ------------------------------------------------------------------
    def handle_incident(self, incident_type: str, context: Dict[str, Any]) -> Dict[str, Any]:

        if incident_type not in self.incident_types:
            return {"status": "unknown_incident_type"}

        config = self.incident_types[incident_type]
        start_time = datetime.now()

        logger.info(
            "Handling %s incident (severity: %s)",
            incident_type,
            config["severity"],
        )

        results: Dict[str, Any] = {
            "incident_type": incident_type,
            "severity": config["severity"],
            "start_time": start_time.isoformat(),
            "steps_executed": [],
            "auto_recovery_attempted": config["auto_response"],
            "escalations_triggered": [],
        }

        # Ejecutar pasos
        for step in config["steps"]:
            step_result = self._execute_step(step, context)
            results["steps_executed"].append(step_result)

            if not step_result["success"]:
                logger.error("Step %s failed", step)
                break

        # Verificar resolución
        resolved = self._verify_resolution(incident_type, context)
        results["resolved"] = resolved

        end_time = datetime.now()
        results["end_time"] = end_time.isoformat()
        results["duration_seconds"] = (end_time - start_time).total_seconds()

        # Escalar si falla
        if not resolved:
            triggered = self._escalate_incident(
                results["severity"],
                results["duration_seconds"],
            )
            results["escalations_triggered"] = triggered

        return results

    # ------------------------------------------------------------------
    # Ejecución de pasos
    # ------------------------------------------------------------------
    def _execute_step(self, step_name: str, context: Dict[str, Any]) -> Dict[str, Any]:

        step_functions = {
            "check_airflow_scheduler": lambda: self._check_service("airflow-scheduler"),
            "check_database_connectivity": lambda: self._check_database_connection(),
            "restart_failed_services": lambda: self._restart_services(
                ["airflow-scheduler", "airflow-webserver"]
            ),
            "verify_pipeline_recovery": lambda: self._verify_pipeline_status(),
            "isolate_affected_data": lambda: self._isolate_bad_data(),
            "check_upstream_sources": lambda: self._check_upstream_sources(context),
            "implement_data_filters": lambda: self._implement_data_filters(context),
            "notify_data_consumers": lambda: self._notify_data_consumers(context),
            "check_resource_usage": lambda: self._check_system_resources(),
            "scale_resources_if_needed": lambda: self._scale_resources(),
            "optimize_running_queries": lambda: self._optimize_running_queries(context),
            "monitor_recovery": lambda: self._monitor_recovery(context),
        }

        try:
            func = step_functions.get(step_name)
            if not func:
                return {"step": step_name, "success": False, "error": "Step not implemented"}

            result = func()
            return {"step": step_name, "success": True, "result": result}

        except Exception as e:
            return {"step": step_name, "success": False, "error": str(e)}

    # ------------------------------------------------------------------
    # Escalamiento
    # ------------------------------------------------------------------
    def _escalate_incident(self, severity: str, duration_seconds: float) -> List[str]:

        escalation_rules = self.escalation_matrix.get(severity, {})
        triggered_actions: List[str] = []

        for threshold, action in escalation_rules.items():
            seconds = self._parse_time_to_seconds(threshold)

            if duration_seconds >= seconds:
                logger.warning("Escalating incident: %s", action)
                triggered_actions.append(action)

        return triggered_actions

    # ------------------------------------------------------------------
    # Funciones simuladas
    # ------------------------------------------------------------------
    def _check_service(self, service_name: str):
        return {"service": service_name, "status": "running"}

    def _check_database_connection(self):
        return {"connected": True}

    def _restart_services(self, services: List[str]):
        return {"restarted": services}

    def _verify_pipeline_status(self):
        return {"pipelines_failed": 0}

    def _isolate_bad_data(self):
        return {"isolated_records": 100}

    def _check_system_resources(self):
        return {"cpu_percent": 40}

    def _scale_resources(self):
        return {"scaled": True}

    def _check_upstream_sources(self, context):
        return {"sources_ok": True}

    def _implement_data_filters(self, context):
        return {"filters_applied": True}

    def _notify_data_consumers(self, context):
        return {"notified": True}

    def _optimize_running_queries(self, context):
        return {"queries_optimized": True}

    def _monitor_recovery(self, context):
        return {"status": "stable"}

    # ------------------------------------------------------------------
    # Verificación resolución
    # ------------------------------------------------------------------
    def _verify_resolution(self, incident_type: str, context: Dict[str, Any]) -> bool:
        return not context.get("force_unresolved", False)

    # ------------------------------------------------------------------
    # Conversión tiempos
    # ------------------------------------------------------------------
    def _parse_time_to_seconds(self, time_str: str) -> int:
        time_str = time_str.lower()

        if time_str.endswith("min"):
            return int(time_str.replace("min", "")) * 60

        if time_str.endswith("h"):
            return int(time_str.replace("h", "")) * 3600

        return 0


# ----------------------------------------------------------------------
# Configuración logging
# ----------------------------------------------------------------------
def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
