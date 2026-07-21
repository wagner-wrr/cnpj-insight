from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.cnpj_service import CNPJAPIError, CNPJNotFoundError, CNPJService

client = TestClient(app)

def test_consulta_cnpj_integra_router_service_e_repository():
    resposta_api_externa = {
        "cnpj": "11222333000181",
        "razao_social": "EMPRESA TESTE LTDA",
        "nome_fantasia": "EMPRESA TESTE",
        "situacao": "ATIVA",
        "municipio": "São Paulo",
        "uf": "SP",
    }

    with patch(
        "app.services.cnpj_service.httpx.AsyncClient"
    ) as cliente_http:
        resposta_mock = Mock()
        resposta_mock.status_code = 200
        resposta_mock.json.return_value = resposta_api_externa

        cliente_http.return_value.__aenter__.return_value.get.return_value = (
            resposta_mock
        )

        resposta = client.get("/cnpj/11222333000181")

    assert resposta.status_code == 200
    assert resposta.json()["cnpj"] == "11222333000181"

def test_consultar_cnpj_retorna_400_para_cnpj_invalido(client, monkeypatch):
    def fake_consultar(self, cnpj):
        raise ValueError("CNPJ inválido. Certifique-se de fornecer um CNPJ válido.")

    monkeypatch.setattr(CNPJService, "consultar", fake_consultar)

    response = client.get("/cnpj/00000000000000")

    assert response.status_code == 400
    assert "CNPJ inválido" in response.json()["detail"]

def test_consultar_cnpj_retorna_404(client, monkeypatch):
    def fake_consultar(self, cnpj):
        raise CNPJNotFoundError("CNPJ não encontrado.")
    
    monkeypatch.setattr(CNPJService, "consultar", fake_consultar)

    response = client.get("/cnpj/11222333000181")

    assert response.status_code == 404
    assert response.json()["detail"] == "CNPJ não encontrado."

def test_consultar_cnpj_retorna_502(client, monkeypatch):
    def fake_consultar(self, cnpj):
        raise CNPJAPIError("Não foi possível conectar à API pública.")

    monkeypatch.setattr(CNPJService, "consultar", fake_consultar)

    response = client.get("/cnpj/11222333000181")

    assert response.status_code == 502
    assert response.json()["detail"] == "Não foi possível conectar à API pública."

def test_favoritar_retorna_404_quando_nao_encontra(client, monkeypatch):
    def fake_favoritar(self, cnpj):
        raise CNPJNotFoundError(
            f"CNPJ {cnpj} não encontrado no histórico para favoritar."
        )
    
    monkeypatch.setattr(CNPJService, "favoritar", fake_favoritar)

    response = client.post("/cnpj/112223330000181/favoritar")

    assert response.status_code == 404
    assert "não encontrado no histórico para favoritar" in response.json()["detail"]

def test_desfavoritar_retorna_404_quando_nao_encontra(client, monkeypatch):
    def fake_desfavoritar(self, cnpj):
        raise CNPJNotFoundError(
            f"CNPJ {cnpj} não está favoritado ou não encontrado."
        )
    
    monkeypatch.setattr(CNPJService, "desfavoritar", fake_desfavoritar)

    response = client.post("/cnpj/11222333000181/desfavoritar")

    assert response.status_code == 404
    assert "não está favoritado ou não encontrado" in response.json()["detail"]
    