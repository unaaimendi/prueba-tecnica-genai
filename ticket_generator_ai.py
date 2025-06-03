import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import json
import re
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import spacy

# Cargar modelo de NER para anonimizar
nlp = spacy.load("en_core_web_sm")

# Cargar clave API desde variable de entorno

app = FastAPI(title="Informe a JSON GPT Processor")

class ReportRequest(BaseModel):
    caseID: str
    reportText: str

class TicketResponse(BaseModel):
    caseID: str
    status: str
    actions: Optional[str] = None
    info: Optional[str] = None
    department: Optional[str] = None

# Función para anonimizar datos personales con expresiones regulares y spaCy
def anonymize_text(text):
    # Eliminar correos y teléfonos
    text = re.sub(r"\b[\w.-]+@[\w.-]+\.\w+\b", "[EMAIL]", text)
    text = re.sub(r"\b\d{9,}\b", "[PHONE]", text)

    # Anonimizar nombres con spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "GPE", "ORG"):
            text = text.replace(ent.text, f"[{ent.label_}]")
    return text

# Función que envía el informe a GPT-4 y devuelve el JSON procesado
def process_with_gpt(caseID, reportText):
    anonymized = anonymize_text(reportText)

    prompt = f"""
Eres un asistente especializado en soporte técnico de móviles. Analiza el siguiente informe técnico y genera un JSON con esta estructura:

{{
  "caseID": "{caseID}",
  "status": "done | pending",
  "actions": "(si aplica)",
  "info": "(información adicional útil)",
  "department": "(si aplica)"
}}

El informe:
"""
    prompt += anonymized

    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente que estructura informes técnicos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0)

        content = response.choices[0].message.content
        data = json.loads(content)

        # Validación básica de campos
        return TicketResponse(
            caseID=caseID,
            status=data.get("status"),
            actions=data.get("actions"),
            info=data.get("info"),
            department=data.get("department")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_ticket", response_model=TicketResponse)
def generate_ticket(req: ReportRequest):
    return process_with_gpt(req.caseID, req.reportText)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
