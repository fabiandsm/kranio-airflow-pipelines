from incident_response.runbook import IncidentRunbook


def test_unknown_incident_type():
    rb = IncidentRunbook()
    res = rb.handle_incident("no_existe", {})
    assert res["status"] == "unknown_incident_type"


def test_parse_time_to_seconds():
    rb = IncidentRunbook()
    assert rb._parse_time_to_seconds("5min") == 300
    assert rb._parse_time_to_seconds("2h") == 7200


def test_escalation_when_unresolved():
    rb = IncidentRunbook()

    # simulamos incidente no resuelto
    actions = rb._escalate_incident("CRITICAL", 2400)

    assert "alert_lead_engineer" in actions


def test_pipeline_down_success():
    rb = IncidentRunbook()
    res = rb.handle_incident("pipeline_down", {})

    assert res["resolved"] is True
    assert len(res["steps_executed"]) > 0
