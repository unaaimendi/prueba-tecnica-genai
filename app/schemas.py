from pydantic import BaseModel
from typing import Literal


class Department(BaseModel):
    """
    Representa un departamento al que puede asignarse un ticket.

    Atributos:
        departmentID (str): Identificador único del departamento.
        description (str): Descripción del departamento o su función.
    """
    departmentID: str
    description: str


class Case(BaseModel):
    """
    Representa un caso de entrada que contiene un informe o reporte.

    Atributos:
        caseID (str): Identificador único del caso.
        report (str): Texto del informe original que describe el problema o situación.
    """
    caseID: str
    report: str


class ReportRequest(BaseModel):
    """
    Modelo para solicitudes que contienen el ID de un caso sobre el cual se generará un ticket.

    Atributos:
        caseID (str): Identificador del caso a procesar.
    """
    caseID: str


class TicketResponse(BaseModel):
    """
    Modelo de respuesta generado tras procesar un caso con un modelo de lenguaje.

    Atributos:
        caseID (str): Identificador del caso original.
        status (Literal["done", "pending"]): Estado del ticket (completado o pendiente).
        actions (str): Acciones sugeridas a tomar.
        info (str): Información adicional relevante para el ticket.
        department (str): Departamento al que se asigna el ticket.
    """
    caseID: str
    status: Literal["done", "pending"]
    actions: str
    info: str
    department: str
