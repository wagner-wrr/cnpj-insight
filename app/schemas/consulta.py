from datetime import datetime

from sqlmodel import SQLModel


class ConsultaResponse(SQLModel):
    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: str | None = None
    situacao: str
    cidade: str
    uf: str
    favorito: bool
    consulta_em: datetime