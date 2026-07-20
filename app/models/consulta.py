from datetime import datetime

from sqlmodel import Field, SQLModel

from app.core.config import settings


class Consulta(SQLModel, table=True):
    """Representa uma consulta de CNPj realizada"""

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    cnpj: str = Field(
        index=True,
        max_length=14,
    )

    razao_social: str

    nome_fantasia: str | None = None

    situacao: str

    cidade: str

    uf: str = Field(max_length=2)

    favorito: bool = Field(default=False) #<- novo campo

    consulta_em: datetime = Field(
        default_factory=lambda: datetime.now(settings.tz),
    )