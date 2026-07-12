from fastapi import FastAPI

from app.routers.home import router as home_router

app = FastAPI(
    title="CNPJ Insigth",
    description="Sistema profissional de consulta de CNPJ",
    version="0.1.0"
)

app.include_router(home_router)