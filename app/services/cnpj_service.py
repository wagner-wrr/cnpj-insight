from typing import Any

import httpx

from app.core.config import settings

from app.utils.cnpj_valida import limpar_cnpj, validar_cnpj

class CNPJNotFoundError(Exception):
    """Exceção lançada quando o CNPJ não é encontrado na API pública."""
    
class CNPJAPIError(Exception):
    """Exceção lançada quando ocorre uma falha na API de CNPJ."""

class CNPJService:
    """Serviço responsável por consultar CNPJs."""

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.base_url = settings.api_url.rstrip("/")

    def consultar(self, cnpj: str) -> dict[str, Any]:
        """Consulta um CNPJ na API pública."""

        cnpj_limpo = limpar_cnpj(cnpj)

        if not validar_cnpj(cnpj_limpo):
            raise ValueError(
                "CNPJ inválido. Certifique-se de fornecer um CNPJ válido."
            )    
        
        url = f"{self.base_url}/{cnpj_limpo}"

        try:

            response = httpx.get(
                url, 
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()
        
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 404:
                raise CNPJNotFoundError(
                    "CNPJ não encontrado."
                ) from exc

            raise CNPJAPIError(
                f"A API pública retornou o status {status_code}."
            ) from exc
        
        except httpx.TimeoutException as exc:
            raise CNPJAPIError(
                "A consulta demorou mais do que o esperado."
            ) from exc

        except httpx.RequestError as exc:
            raise CNPJAPIError(
                "Não foi possível conectar à API pública."
            ) from exc
        