from app.services.cnpj_service import CNPJAPIError, CNPJNotFoundError, CNPJService

def test_historico_retorna_200_e_lista(client, monkeypatch):
    def fake_listar_historico(self, limite=20):
        assert limite == 20
        return [
            {
                "id": 1,
                "cnpj": "11222333000181",
                "razao_social": "EMPRESA A",
                "nome_fantasia": "A",
                "situacao": "ATIVA",
                "cidade": "Eunápolis",
                "uf": "BA",
                "favorito": False,
                "consulta_em": "2026-07-19T10:00:00",
            }
        ]
    
    monkeypatch.setattr(CNPJService, "listar_historico", fake_listar_historico)

    response = client.get("/cnpj/historico")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["cnpj"] == "11222333000181"

def test_listar_historico_respeita_limite(client, monkeypatch):
    def fake_listar_historico(self, limite=20):
        assert limite == 5
        return []
    
    monkeypatch.setattr(CNPJService, "listar_historico", fake_listar_historico)

    response = client.get("/cnpj/historico?limite=5")

    assert response.status_code == 200
    assert response.json() ==[]    

def test_listar_historico_rejeita_limite_maior_que_100(client):
    response = client.get("/cnpj/historico?limite=101")

    assert response.status_code ==422
    
def test_get_estatisticas_retorna_200_e_payload(client, monkeypatch):
    def fake_obter_estatisticas(self):
        return {
            "total_consultas":10,
            "total_favoritos":3,
        }

    monkeypatch.setattr(CNPJService, "obter_estatisticas", fake_obter_estatisticas)

    response = client.get("/cnpj/estatisticas")

    assert response.status_code == 200
    assert response.json() == {
        "total_consultas":10,
        "total_favoritos":3,
    }

def test_post_favoritar_retorna_200_e_lista(client, monkeypatch):
    def fake_listar_favoritos(self, limite=20):
        assert limite == 20
        return [
            {
                "id":2,
                "cnpj":"22333444000199",
                "razao_social":"EMPRESA FAVORITA",
                "nome_fantasia":"FAVORITA",
                "situacao":"ATIVA",
                "cidade":"Porto Seguro",
                "uf":"BA",
                "favorito": True,
                "consulta_em":"2026-07-19T11:00:00",
            }
        ]
    
    monkeypatch.setattr(CNPJService, "listar_favoritos", fake_listar_favoritos)

    response = client.get("/cnpj/favoritos")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["favorito"] is True
    assert data[0]["cnpj"] == "22333444000199"

def test_favoritar_retorna_200_e_limpa_cnpj(client, cnpj_exemplo, monkeypatch):
    def fake_favoritar(self, cnpj):
        assert cnpj == "11222333000181"
        return {
            "mensagem":"CNPJ 11222333000181 favoritado com sucesso",
            "consulta":{
                "id":1,
                "cnpj":"11222333000181",
                "razao_social":"EMPRESA TESTE LTDA",
            }
        }
    
    monkeypatch.setattr(CNPJService, "favoritar", fake_favoritar)

    response = client.post(f"/cnpj/{cnpj_exemplo}/favoritar")

    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert data["consulta"]["cnpj"] == "11222333000181"

def test_favoritar_retorna_404_quando_nao_encontra(client, monkeypatch):
    def fake_favoritar(self, cnpj):
        raise CNPJNotFoundError(
            f"CNPJ {cnpj} não encontrado no histórico para favoritar."
        )
    
    monkeypatch.setattr(CNPJService, "favoritar", fake_favoritar)

    response = client.post("/cnpj/112223330000181/favoritar")

    assert response.status_code == 404
    assert "não encontrado no histórico para favoritar" in response.json()["detail"]
    
def test_post_desfavoritar_retorna_200_e_limp_cnpj(client, cnpj_exemplo, monkeypatch):
    def fake_desfavoritar(self, cnpj):
        assert cnpj == "11222333000181"
        return {
            "mensagem":"CNPJ removido dos favoritos",
            "cnpj":cnpj
        }
    
    monkeypatch.setattr(CNPJService, "desfavoritar", fake_desfavoritar)

    response = client.post(f"/cnpj/{cnpj_exemplo}/desfavoritar")

    assert response.status_code == 200
    data = response.json()
    assert data["mensagem"] == "CNPJ removido dos favoritos"

def test_desfavoritar_retorna_404_quando_nao_encontra(client, monkeypatch):
    def fake_desfavoritar(self, cnpj):
        raise CNPJNotFoundError(
            f"CNPJ {cnpj} não está favoritado ou não encontrado."
        )
    
    monkeypatch.setattr(CNPJService, "desfavoritar", fake_desfavoritar)

    response = client.post("/cnpj/11222333000181/desfavoritar")

    assert response.status_code == 404
    assert "não está favoritado ou não encontrado" in response.json()["detail"]

def test_consultar_cnpj_retorna_200(client, monkeypatch):
    def fake_consultar(self, cnpj):
        assert cnpj == "11222333000181"
        return {
                "id": 1,
                "cnpj": "11222333000181",
                "razao_social": "EMPRESA A",
                "nome_fantasia": "A",
                "situacao": "ATIVA",
                "cidade": "Eunápolis",
                "uf": "BA",
                "consulta_em": "2026-07-19T10:00:00",
        }
    
    monkeypatch.setattr(CNPJService, "consultar", fake_consultar)

    response = client.get("/cnpj/11222333000181")

    assert response.status_code == 200
    data = response.json()
    assert data["cnpj"] == "11222333000181"
    assert data["razao_social"] == "EMPRESA A"

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

def test_consultar_cnpj_retorna_400_para_cnpj_invalido(client, monkeypatch):
    def fake_consultar(self, cnpj):
        raise ValueError("CNPJ inválido. Certifique-se de fornecer um CNPJ válido.")

    monkeypatch.setattr(CNPJService, "consultar", fake_consultar)

    response = client.get("/cnpj/00000000000000")

    assert response.status_code == 400
    assert "CNPJ inválido" in response.json()["detail"]