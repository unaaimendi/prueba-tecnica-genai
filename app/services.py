from openai import OpenAI
from app.schemas import TicketResponse, Case, Department
from app.utils import load_cases, load_departments
from app.anonymizer import anonymize
from string import Template
from pathlib import Path
import os
import json
import yaml

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_prompt(path: str, replacements: dict) -> dict:
    """
    Carga un prompt desde un archivo YAML y aplica sustituciones en los campos 'system' y 'user'.

    Args:
        path (str): Ruta al archivo YAML que contiene los mensajes del prompt.
        replacements (dict): Diccionario con las variables a sustituir en los mensajes.

    Returns:
        dict: Diccionario con dos claves, 'system' y 'user', que contienen los mensajes procesados.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return {
        "system": Template(data["system"]).substitute(replacements),
        "user": Template(data["user"]).substitute(replacements),
    }


def generate_ticket_from_openai(case_id: str) -> TicketResponse:
    """
    Genera un ticket a partir del informe de un caso utilizando un modelo de lenguaje (OpenAI GPT).

    Args:
        case_id (str): ID del caso para el cual se generará el ticket.

    Returns:
        TicketResponse: Objeto que representa el ticket generado a partir del informe anonimizado.

    Raises:
        ValueError: Si no se encuentra el caso con el ID proporcionado o si la respuesta de OpenAI es inválida.
    """
    cases: list[Case] = load_cases()
    departments: list[Department] = load_departments()

    case = next((c for c in cases if c.caseID == case_id), None)
    if not case:
        raise ValueError(f"Case with ID {case_id} not found.")

    report = anonymize(case.report)
    dept_info = "\n".join([f"- {d.departmentID}: {d.description}" for d in departments])
    dept_ids = ", ".join([d.departmentID for d in departments])

    prompt_messages = load_prompt(
        "prompt/ticket_prompt.yml",
        {
            "departments_info": dept_info,
            "departments_list": dept_ids,
            "report": report
        }
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_messages["system"]},
            {"role": "user", "content": prompt_messages["user"]}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
    except Exception as e:
        raise ValueError(f"Respuesta de OpenAI inválida:\n{content}") from e

    return TicketResponse(**parsed)
