from datetime import datetime

from sqlalchemy import func
from sqlmodel import Session, select, func

from app.core.config import settings
from app.models.consulta import Consulta


class ConsultaRepository:
    """Resposável por persistir consultas no banco."""

    def __init__(self, session: Session):
        self.session= session

    def salvar(self, consulta: Consulta) -> Consulta:
        """Salva uma consulta no banco de dados.""" 

        self.session.add(consulta)
        self.session.commit()
        self.session.refresh(consulta)

        return consulta
    
    def listar(self, limite: int = 20) -> list[Consulta]:
        """Retorna as consultas mas recentes"""
        return self.session.exec(
            select(Consulta)
            .order_by(Consulta.consulta_em.desc())
            .limit(limite)
        ).all()
    
    def estatisticas(self) -> dict:
        """Retorna estatísticas completas das consultas."""

        total = self.session.exec(
            select(func.count(Consulta.id))
        ).one()

        total_favoritos = self.session.exec(
        select(func.count())
        .select_from(Consulta)
        .where(Consulta.favorito.is_(True))
        ).one()

        hoje = datetime.now(settings.tz).date()
        consultas_hoje = self.session.exec(
            select(func.count(Consulta.id))
            .where(func.date(Consulta.consulta_em) == hoje)
        ).one()

        por_uf = self.session.exec(
            select(Consulta.uf, func.count(Consulta.id).label("total"))
            .group_by(Consulta.uf)
            .order_by(func.count(Consulta.id).desc())
        ).all()

        por_situacao = self.session.exec(
            select(Consulta.situacao, func.count(Consulta.id).label("total"))
            .group_by(Consulta.situacao)
            .order_by(func.count(Consulta.id).desc())
        ).all()

        mais_consultas = self.session.exec(
            select(
                Consulta.cnpj,
                Consulta.razao_social,
                func.count(Consulta.id).label("total"),
            )
            .group_by(Consulta.cnpj, Consulta.razao_social)
            .order_by(func.count(Consulta.id).desc())
            .limit(10)
        ).all()

        return{
            "total_consultas": total,
            "total_favoritos": total_favoritos,
            "consultas_hoje": consultas_hoje,
            "por_uf":[
                {"uf": uf or "N/I", "total":total_uf}
                for uf, total_uf in por_uf
            ],
            "por_situacao":[
                {"situacao": situacao or "N/I", "total":total_sit}
                for situacao, total_sit in por_situacao
            ],
            "mais_consultas":[
                {"cnpj":cnpj, "razao_social": razao, "total":t}
                for cnpj, razao, t in mais_consultas
            ],
        }
    def favoritar(self, cnpj: str) -> Consulta | None:
        """Marcar a consulta mais recente do CNPJ como favorita"""
        consulta = self.session.exec(
            select(Consulta)
            .where(Consulta.cnpj == cnpj)
            .order_by(Consulta.consulta_em.desc())
            .limit(1)
        ).first()

        if consulta:
            consulta.favorito = True
            self.session.commit()
            self.session.refresh(consulta)

            return consulta
        
    def desfavoritar(self, cnpj: str) -> Consulta | None:
        """Remove o favorito do CNPJ."""
        consultas = self.session.exec(
            select(Consulta)
            .where(Consulta.cnpj == cnpj)
            .where(Consulta.favorito)
    ).all()

        if not consultas:
            return None
            
        for c in consultas:
            c.favorito = False
        self.session.commit()

        return consultas[0]
        
    def listar_favoritos(self, limite: int = 20) -> list[Consulta]:
        """Retorna os CNPJs favoritados (um por CNPJ, o mais recente)."""
        return self.session.exec(
        select(Consulta)
        .where(Consulta.favorito)
        .order_by(Consulta.consulta_em.desc())
        .limit(limite)
    ).all()
            