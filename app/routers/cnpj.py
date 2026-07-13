from typing import Any

from fastapi import APIRouter, HTTPException, status    

from app.services.cnpj_service import (
    CNPJAPIError,
    CNPJNotFoundError, 
    CNPJService,  
)

router = APIRouter(
    prefix="/cnpj",
    tags=["CNPJ"],
)

service = CNPJService()


@router.get("/{cnpj}", response_model=dict[str, Any])
def consultar_cnpj(cnpj: str) -> dict[str, Any]:
    """Consulta os dados de uma empresa pelo CNPJ na API pública."""

    try:
        return service.consultar(cnpj)
    
    except CNPJNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
  
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )