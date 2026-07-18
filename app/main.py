from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.database.connection import create_db_and_tables
from app.routers.cnpj import router as cnpj_router
from app.routers.health import router as health_router
from app.routers.home import router as home_router

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:  
    """Executa tarefas de inicialização e encerramento."""

    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema profissional de consulta de CNPJ.",
    lifespan=lifespan,
)

app.include_router(home_router)
app.include_router(health_router)
app.include_router(cnpj_router)