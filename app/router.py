from fastapi import APIRouter, HTTPException
from app.schemas import ReportRequest, TicketResponse
from app.services import generate_ticket_from_openai

# Enrutador de FastAPI para gestionar las rutas relacionadas con los tickets
router = APIRouter()


@router.post("/ticket", response_model=TicketResponse)
def create_ticket(req: ReportRequest):
    """
    Crea un ticket a partir del contenido de un caso mediante un modelo de lenguaje (OpenAI).

    Args:
        req (ReportRequest): Objeto que contiene el ID del caso a procesar.

    Returns:
        TicketResponse: Estructura con los campos generados por el modelo, como título, descripción,
                        estado, acciones sugeridas, etc.

    Raises:
        HTTPException: Si ocurre un error durante el procesamiento (por ejemplo, ID inválido o error de red),
                       se devuelve un error HTTP 500 con el detalle del problema.
    """
    try:
        return generate_ticket_from_openai(req.caseID)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
