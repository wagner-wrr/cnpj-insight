from datetime import datetime
from typing import Any

from sqlalchemy import func
from sqlmodel import Session, col, select

from app.core.config import settings
from app.models.consulta import Consulta


class ConsultaRepository:
    """Responsável por persistir consultas no banco de dados."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def salvar(self, consulta: Consulta) -> Consulta:
        """Salva uma consulta no banco de dados."""

        self.session.add(consulta)
        self.session.commit()
        self.session.refresh(consulta)

        return consulta

    def listar(self, limite: int = 20) -> list[Consulta]:
        """Retorna as consultas mais recentes."""

        consultas = self.session.exec(
            select(Consulta)
            .order_by(
                col(Consulta.consulta_em).desc(),
                col(Consulta.id).desc(),
            )
            .limit(limite)
        ).all()

        return list(consultas)

    def estatisticas(self) -> dict[str, Any]:
        """Retorna estatísticas completas das consultas."""

        total = self.session.exec(
            select(func.count())
            .select_from(Consulta)
        ).one()

        total_favoritos = self.session.exec(
            select(func.count())
            .select_from(Consulta)
            .where(col(Consulta.favorito).is_(True))
        ).one()

        hoje = datetime.now(settings.tz).date().isoformat()

        consultas_hoje = self.session.exec(
            select(func.count())
            .select_from(Consulta)
            .where(
                func.date(col(Consulta.consulta_em)) == hoje
            )
        ).one()

        por_uf = self.session.exec(
            select(
                col(Consulta.uf),
                func.count().label("total"),
            )
            .select_from(Consulta)
            .group_by(col(Consulta.uf))
            .order_by(func.count().desc())
        ).all()

        por_situacao = self.session.exec(
            select(
                col(Consulta.situacao),
                func.count().label("total"),
            )
            .select_from(Consulta)
            .group_by(col(Consulta.situacao))
            .order_by(func.count().desc())
        ).all()

        mais_consultadas = self.session.exec(
            select(
                col(Consulta.cnpj),
                col(Consulta.razao_social),
                func.count().label("total"),
            )
            .select_from(Consulta)
            .group_by(
                col(Consulta.cnpj),
                col(Consulta.razao_social),
            )
            .order_by(func.count().desc())
            .limit(10)
        ).all()

        return {
            "total_consultas": total,
            "total_favoritos": total_favoritos,
            "consultas_hoje": consultas_hoje,
            "por_uf": [
                {
                    "uf": uf or "N/I",
                    "total": total_uf,
                }
                for uf, total_uf in por_uf
            ],
            "por_situacao": [
                {
                    "situacao": situacao or "N/I",
                    "total": total_situacao,
                }
                for situacao, total_situacao in por_situacao
            ],
            "mais_consultadas": [
                {
                    "cnpj": cnpj,
                    "razao_social": razao_social,
                    "total": total_cnpj,
                }
                for cnpj, razao_social, total_cnpj in mais_consultadas
            ],
        }

    def favoritar(self, cnpj: str) -> Consulta | None:
        """Marca a consulta mais recente do CNPJ como favorita."""

        consulta = self.session.exec(
            select(Consulta)
            .where(col(Consulta.cnpj) == cnpj)
            .order_by(
                col(Consulta.consulta_em).desc(),
                col(Consulta.id).desc(),
            )
            .limit(1)
        ).first()

        if consulta is None:
            return None

        consulta.favorito = True

        self.session.add(consulta)
        self.session.commit()
        self.session.refresh(consulta)

        return consulta

    def desfavoritar(self, cnpj: str) -> Consulta | None:
        """Remove todas as marcações de favorito do CNPJ."""

        resultado = self.session.exec(
            select(Consulta)
            .where(col(Consulta.cnpj) == cnpj)
            .where(col(Consulta.favorito).is_(True))
            .order_by(
                col(Consulta.consulta_em).desc(),
                col(Consulta.id).desc(),
            )
        ).all()

        consultas = list(resultado)

        if not consultas:
            return None

        for consulta in consultas:
            consulta.favorito = False
            self.session.add(consulta)

        self.session.commit()

        consulta_mais_recente = consultas[0]
        self.session.refresh(consulta_mais_recente)

        return consulta_mais_recente

    def listar_favoritos(
        self,
        limite: int = 20,
    ) -> list[Consulta]:
        """Retorna as consultas marcadas como favoritas."""

        favoritos = self.session.exec(
            select(Consulta)
            .where(col(Consulta.favorito).is_(True))
            .order_by(
                col(Consulta.consulta_em).desc(),
                col(Consulta.id).desc(),
            )
            .limit(limite)
        ).all()

        return list(favoritos)