from fastapi import APIRouter, HTTPException
from app.schemas import ReportRequest, TicketResponse
from app.services import generate_ticket_from_openai

router = APIRouter()


@router.post("/ticket", response_model=TicketResponse)
def create_ticket(req: ReportRequest):
    try:
        return generate_ticket_from_openai(req.caseID)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
