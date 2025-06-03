import json
import pytest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
from app.services import generate_ticket_from_openai
from app.schemas import TicketResponse


@patch("app.services.client.chat.completions.create")
@patch("app.services.load_cases")
@patch("app.services.load_departments")
@patch("app.services.load_prompt")
@patch("app.services.anonymize")
def test_generate_ticket_from_openai_success(
    mock_anonymize, mock_load_prompt, mock_load_departments,
    mock_load_cases, mock_openai
):
    # Mock input data
    mock_case = MagicMock()
    mock_case.caseID = "case123"
    mock_case.report = "Informe confidencial de Juan Pérez"
    mock_load_cases.return_value = [mock_case]

    mock_department = MagicMock()
    mock_department.departmentID = "dept1"
    mock_department.description = "Departamento de Pruebas"
    mock_load_departments.return_value = [mock_department]

    mock_anonymize.return_value = "Informe confidencial de [name]"

    mock_load_prompt.return_value = {
        "system": "Sistema prompt",
        "user": "Usuario prompt"
    }

    mock_openai.return_value = SimpleNamespace(
    choices=[
        SimpleNamespace(
            message=SimpleNamespace(
                content=json.dumps({
                    "caseID": "case123",
                    "status": "done",
                    "actions": "Enviar el dispositivo a nuestro centro",
                    "info": "Información adicional",
                    "department": "dept1"
                })
            )
        )
    ]
)

    response = generate_ticket_from_openai("case123")

    assert isinstance(response, TicketResponse)
    assert response.caseID == "case123"
    assert response.status == "done"
    assert response.department == "dept1"

@patch("app.services.load_cases")
def test_generate_ticket_from_openai_case_not_found(mock_load_cases):
    mock_load_cases.return_value = []
    with pytest.raises(ValueError, match="Case with ID case999 not found."):
        generate_ticket_from_openai("case999")


@patch("app.services.client.chat.completions.create")
@patch("app.services.load_cases")
@patch("app.services.load_departments")
@patch("app.services.load_prompt")
@patch("app.services.anonymize")
def test_generate_ticket_from_openai_invalid_json(
    mock_anonymize, mock_load_prompt, mock_load_departments,
    mock_load_cases, mock_openai
):
    mock_case = MagicMock()
    mock_case.caseID = "case123"
    mock_case.report = "Texto"
    mock_load_cases.return_value = [mock_case]

    mock_department = MagicMock()
    mock_department.departmentID = "dept1"
    mock_department.description = "Dep"
    mock_load_departments.return_value = [mock_department]

    mock_anonymize.return_value = "Texto [anon]"

    mock_load_prompt.return_value = {
        "system": "Sistema",
        "user": "Usuario"
    }

    # Devuelve texto que no es JSON
    mock_openai.return_value = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Texto que no es JSON válido"
                )
            )
        ]
    )

    with pytest.raises(ValueError, match="Respuesta de OpenAI inválida"):
        generate_ticket_from_openai("case123")
