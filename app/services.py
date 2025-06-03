from openai import OpenAI
from app.schemas import TicketResponse
from app.utils import load_cases, load_departments
import os
import json
from app.anonymizer import anonymize

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ticket_from_openai(case_id: str) -> TicketResponse:
    cases = load_cases()
    departments = load_departments()

    case = next((c for c in cases if c.caseID == case_id), None)
    if not case:
        raise ValueError(f"Case with ID {case_id} not found.")

    report = anonymize(case.report)  # 👈 Anonimización del informe

    dept_info = "\n".join(
        [f"- {d.departmentID}: {d.description}" for d in departments]
    )

    prompt = f"""
Se te proporciona un informe técnico de un cliente. Debes analizarlo y devolver una respuesta en formato JSON con las siguientes claves:

• caseID: ID del caso
• status: done/pending (indica si el problema ya está resuelto o si requiere acciones)
• actions: resumen conciso pero completo de las acciones requeridas
• info: información relevante adicional para resolver el caso
• department: departamento responsable (usa solo uno de: {[d.departmentID for d in departments]})

---
Departamentos disponibles:
{dept_info}

---
Informe del caso:
{report}

Responde únicamente con el JSON solicitado.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en soporte técnico."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
    except Exception:
        raise ValueError(f"Respuesta de OpenAI inválida: {content}")

    return TicketResponse(**parsed)
