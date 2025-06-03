from pydantic import BaseModel
from typing import Literal


class Department(BaseModel):
    departmentID: str
    description: str


class Case(BaseModel):
    caseID: str
    report: str


class ReportRequest(BaseModel):
    caseID: str


class TicketResponse(BaseModel):
    caseID: str
    status: Literal["done", "pending"]
    actions: str
    info: str
    department: str