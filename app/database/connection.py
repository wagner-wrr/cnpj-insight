from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

connect_args = {
    "check_same_thread": False,
}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,
)

def create_db_and_tables() -> None:   
    """Cria o banco de dados e todas as tabelas registradas."""

    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:    
    """Fornece uma sessão de banco para cada requisição."""
    
    with Session(engine) as session:
        yield session