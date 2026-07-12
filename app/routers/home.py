from fastapi import APIRouter

router = APIRouter()

@router.get ("/")
def home():
    return {
        "projeto": "CNPJ Insigth",
        "version": "0.1.0",
        "status": "Online 🚀"
    }