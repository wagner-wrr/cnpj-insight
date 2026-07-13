from fastapi import FastAPI

from app.core.config import settings
from app.routers.cnpj import router as cnpj_router
from app.routers.health import router as health_router
from app.routers.home import router as home_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema profissional de consulta de CNPJ.",
)

app.include_router(home_router)
app.include_router(health_router)
app.include_router(cnpj_router)