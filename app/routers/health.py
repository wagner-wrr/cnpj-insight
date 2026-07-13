from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health():
    """Rota de verificação da saúde da aplicação."""
    return {
        "status": "healthy"
    }