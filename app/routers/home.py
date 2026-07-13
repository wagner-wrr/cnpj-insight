from fastapi import APIRouter

router = APIRouter(tags=["Home"])


@router.get("/")
def home():
    """Rota inicial da aplicação."""
    return {
        "application": "CNPJ Insight",
        "status": "running",
        "version": "0.1.0",
    }
