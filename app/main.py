from fastapi import FastAPI
from app.router import router


app = FastAPI(
    title="Asignación automática de tickets",
    description="Clasifica reportes y asigna un departamento con acciones sugeridas.",
    version="1.0.0"
)

app.include_router(router)
