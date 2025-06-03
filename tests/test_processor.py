from app.processor import process_report

def test_process_report(monkeypatch):
    # Mock GPT output
    def mock_generate_ticket_json(case_id, report):
        return {
            "caseID": case_id,
            "status": "done",
            "actions": None,
            "info": "Issue resolved after restart.",
            "department": None
        }

    monkeypatch.setattr("app.processor.generate_ticket_json", mock_generate_ticket_json)

    case_id = "ABC123"
    report = "El cliente reinició su móvil y el problema se solucionó."

    result = process_report(case_id, report)
    assert result["caseID"] == case_id
    assert result["status"] == "done"
    assert result["info"] is not None
