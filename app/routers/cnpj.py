from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.database.connection import get_session
from app.models.consulta import Consulta
from app.repositories.consulta_repository import ConsultaRepository
from app.schemas.consulta import ConsultaResponse
from app.services.cnpj_service import CNPJAPIError, CNPJNotFoundError, CNPJService

router = APIRouter(
    prefix="/cnpj",
    tags=["CNPJ"],
)

@router.get("/historico", response_model=list[ConsultaResponse])
def listar_historico(
    limite: int = Query(default=20, ge=1, le=100),
    session:Session = Depends(get_session),
) -> list[Consulta]:
    """Lista o histórico de consultas realizadas, da mais recente para a mais antiga."""
    repository = ConsultaRepository(session)
    service = CNPJService(repository=repository)
    return service.listar_historico(limite=limite)

@router.get("/estatisticas")
def estatisticas(
    session: Session = Depends(get_session),
) -> dict:
    """Retorna estatísticas das consultas realizadas."""

    repository = ConsultaRepository(session)
    service = CNPJService(repository=repository)
    return service.obter_estatisticas()

@router.get("/favoritos", response_model=list[ConsultaResponse])
def listar_favoritos(
    limite: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    ) -> list[Consulta]:
    """Lista os CNPJs favoritados"""
    repository = ConsultaRepository(session)
    service = CNPJService(repository=repository)
    return service.listar_favoritos(limite=limite)

@router.post("/{cnpj}/favoritar")
def favoritar(
    cnpj: str,
    session: Session = Depends(get_session),
) -> dict:
    """Marca um CNPJ como favorito."""
    repository = ConsultaRepository(session)
    service = CNPJService(repository=repository)

    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-","")

    try:
        return service.favoritar(cnpj_limpo)
    except CNPJNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc),
        ) from exc
    
@router.post("/{cnpj}/desfavoritar")
def desfavoritar(
    cnpj: str, 
    session: Session = Depends(get_session),
) -> dict:
    """Remove um CNPJ dos favoritos."""
    repository = ConsultaRepository(session)
    service = CNPJService(repository=repository)

    cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-","")

    try:
        return service.desfavoritar(cnpj_limpo)
    except CNPJNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc),
        ) from exc
    
@router.get("/{cnpj}", response_model=dict[str, Any])
def consultar_cnpj(
    cnpj: str,
    session: Session = Depends(get_session),
) -> dict[str, Any]:
    repository = ConsultaRepository(session)
    service = CNPJService(repository=repository)

    try:
        return service.consultar(cnpj)

    except CNPJNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except CNPJAPIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc