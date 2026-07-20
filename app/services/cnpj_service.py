from typing import Any

import httpx

from app.core.config import settings
from app.models.consulta import Consulta
from app.repositories.consulta_repository import ConsultaRepository
from app.utils.cnpj import limpar_cnpj, validar_cnpj


class CNPJNotFoundError(Exception):
    """Exceção lançada quando o CNPJ não é encontrado na API pública."""
    
class CNPJAPIError(Exception):
    """Exceção lançada quando ocorre uma falha na API de CNPJ."""

class CNPJService:
    """Serviço responsável por consultar CNPJs."""

    def __init__(self, repository=None):
        self.repository = repository or ConsultaRepository()
        self.base_url = settings.api_url.rstrip("/")
        self.timeout = getattr(settings, "api_timeout", 10.0)

    def consultar(self, cnpj: str) -> dict[str, Any]:
        """Consulta um CNPJ na API pública."""

        cnpj_limpo = limpar_cnpj(cnpj)

        if not validar_cnpj(cnpj_limpo):
            raise ValueError(
                "CNPJ inválido. Certifique-se de fornecer um CNPJ válido."
            )    
        
        url = f"{self.base_url}/{cnpj_limpo}"

        try:

            response = httpx.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 404:
                raise CNPJNotFoundError(
                    "CNPJ não encontrado."
                ) from exc

            raise CNPJAPIError(
                f"A API pública retornou o status {exc.response.status_code}."
            ) from exc
        
        except httpx.TimeoutException as exc:
            raise CNPJAPIError(
                "A consulta demorou mais do que o esperado."
            ) from exc

        except httpx.RequestError as exc:
            raise CNPJAPIError(
                "Não foi possível conectar à API pública."
            ) from exc
        
        estabelecimento = data.get("estabelecimento",{})
        cidade = estabelecimento.get("cidade",{}) or {}
        estado = estabelecimento.get("estado",{}) or {}
        
        """--- Integração Service -->Repository ---"""
        consulta = Consulta(
            cnpj=cnpj_limpo,
            razao_social=data.get("razao_social", ""),
            nome_fantasia=estabelecimento.get("nome_fantasia"),
            situacao=estabelecimento.get("situacao_cadastral", ""),
            cidade=cidade.get("nome", ""),
            uf=estado.get("sigla", "")
        )


        consulta_salva = self.repository.salvar(consulta)

        return {
            "id":consulta_salva.id,
            "cnpj":consulta_salva.cnpj,
            "razao_social":consulta_salva.razao_social,
            "nome_fantasia":consulta_salva.nome_fantasia,
            "situacao":consulta_salva.situacao,
            "cidade":consulta_salva.cidade,
            "uf":consulta_salva.uf,
            "consulta_em":consulta_salva.consulta_em.isoformat(),
        }
    

    def listar_historico(self, limite: int = 20) -> list[Consulta]:
        """Retorna o hitórico de consultas realizadas."""
        return self.repository.listar(limite=limite)
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas das consultas."""
        return self.repository.estatisticas()
    def favoritar(self, cnpj: str) -> dict | None:
        """Marca um CNPJ como favorito."""
        consulta = self.repository.favoritar(cnpj)
        if not consulta:
           raise CNPJNotFoundError(
               f"CNPJ {cnpj} não encontrado no histórico para favoritar."
           )
        return {
        "mensagem": f"CNPJ {cnpj} favoritado com sucesso.",
        "consulta": {
            "id": consulta.id,
            "cnpj": consulta.cnpj,
            "razao_social": consulta.razao_social,
        },
    }

    def desfavoritar(self, cnpj: str) -> dict:
        """ Remove um CNPJ dos favoritos."""
        consulta = self.repository.desfavoritar(cnpj)
        if not consulta:
            raise CNPJNotFoundError(
                f"CNPJ {cnpj} não está favoritado ou não encontrado."
            )
        return {
            "mensagem": f"Favorito removido para o CNPJ {cnpj}."
        }
    
    def listar_favoritos(self, limite: int = 20) -> list[Consulta]:
        """ Retorna os CNPJs favoritados."""
        return self.repository.listar_favoritos(limite=limite)