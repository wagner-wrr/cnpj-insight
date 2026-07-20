from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.database.connection import get_session
from app.main import app


@pytest.fixture(autouse=True)
def override_get_sessio():
    def fake_get_session():
        yield Mock()

    app.dependency_overrides[get_session] = fake_get_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def cnpj_exemplo():
    return "11222333000181"

@pytest.fixture
def cnpj_formatado():
    return "11.222.333/0001-81"

@pytest.fixture
def session_test():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session