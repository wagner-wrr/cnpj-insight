from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

import httpx
import pytest

from app.services.cnpj_service import (
    CNPJAPIError,
    CNPJNotFoundError,
    CNPJService,
)


@patch("app.services.cnpj_service.validar_cnpj", return_value=True)
@patch("app.services.cnpj_service.limpar_cnpj", return_value="11222333000181")
@patch("app.services.cnpj_service.httpx.get")
def test_consultar_retorna_dados_mapeados_e_salva_no_repository(
    mock_get, mock_limpar_cnpj, mock_validar_cnpj
):
    repository = Mock()

    consulta_salva = SimpleNamespace(
        id=1,
        cnpj="11222333000181",
        razao_social="EMPRESA TESTE LTDA",
        nome_fantasia="EMPRESA TESTE",
        situacao="ATIVA",
        cidade="São Paulo",
        uf="SP",
        consulta_em=datetime(2026, 7, 19, 12, 0, 0),
    )

    repository.salvar.return_value = consulta_salva

    response_mock = Mock()
    response_mock.raise_for_status.return_value = None
    response_mock.json.return_value = {
        "razao_social": "EMPRESA TESTE LTDA",
        "estabelecimento": {
            "nome_fantasia": "EMPRESA TESTE",
            "situacao_cadastral": "ATIVA",
            "cidade": {"nome": "São Paulo"},
            "estado": {"sigla": "SP"},
        },
    }
    mock_get.return_value = response_mock

    service = CNPJService(repository=repository)

    resultado = service.consultar("11.222.333/0001-81")

    mock_limpar_cnpj.assert_called_once_with("11.222.333/0001-81")
    mock_validar_cnpj.assert_called_once_with("11222333000181")
    mock_get.assert_called_once_with(
        f"{service.base_url}/11222333000181",
        timeout=service.timeout,
    )
    repository.salvar.assert_called_once()

    consulta_enviada = repository.salvar.call_args.args[0]
    assert consulta_enviada.cnpj == "11222333000181"
    assert consulta_enviada.razao_social == "EMPRESA TESTE LTDA"
    assert consulta_enviada.nome_fantasia == "EMPRESA TESTE"
    assert consulta_enviada.situacao == "ATIVA"
    assert consulta_enviada.cidade == "São Paulo"
    assert consulta_enviada.uf == "SP"

    assert resultado == {
        "id": 1,
        "cnpj": "11222333000181",
        "razao_social": "EMPRESA TESTE LTDA",
        "nome_fantasia": "EMPRESA TESTE",
        "situacao": "ATIVA",
        "cidade": "São Paulo",
        "uf": "SP",
        "consulta_em": "2026-07-19T12:00:00",
    }

@patch("app.services.cnpj_service.validar_cnpj", return_value=False)
@patch("app.services.cnpj_service.limpar_cnpj", return_value="00000000000000")
def test_consultar_lanca_value_error_quando_cnpj_invalido(
    mock_limpar_cnpj, mock_validar_cnpj
):
    repository = Mock()
    service = CNPJService(repository=repository)

    with pytest.raises(ValueError, match="CNPJ inválido"):
        service.consultar("00000000000000")

    repository.salvar.assert_not_called()

@patch("app.services.cnpj_service.validar_cnpj", return_value=True)
@patch("app.services.cnpj_service.limpar_cnpj", return_value="11222333000181")
@patch("app.services.cnpj_service.httpx.get")
def test_consultar_lanca_cnpj_not_found_quando_api_retorna_404(
    mock_get, mock_limpar_cnpj, mock_validar_cnpj
):
    request = httpx.Request("GET", "https://fake-api/cnpj/11222333000181")
    response = httpx.Response(404, request=request)

    response_mock = Mock()
    response_mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not found",
        request=request,
        response=response,
    )
    mock_get.return_value = response_mock

    service = CNPJService(repository=Mock())

    with pytest.raises(CNPJNotFoundError, match="CNPJ não encontrado"):
        service.consultar("11222333000181")

@patch("app.services.cnpj_service.validar_cnpj", return_value=True)
@patch("app.services.cnpj_service.limpar_cnpj", return_value="11222333000181")
@patch("app.services.cnpj_service.httpx.get")
def test_consultar_lanca_api_error_quando_timeout(
    mock_get, mock_limpar_cnpj, mock_validar_cnpj
):
    mock_get.side_effect = httpx.TimeoutException("Timeout")

    service = CNPJService(repository=Mock())

    with pytest.raises(CNPJAPIError, match="demorou mais do que o esperado"):
        service.consultar("11222333000181")

@patch("app.services.cnpj_service.validar_cnpj", return_value=True)
@patch("app.services.cnpj_service.limpar_cnpj", return_value="11222333000181")
@patch("app.services.cnpj_service.httpx.get")
def test_consultar_lanca_api_error_quando_falha_de_conexao(
    mock_get, mock_limpar_cnpj, mock_validar_cnpj
):
    request = httpx.Request("GET", "https://fake-api/cnpj/11222333000181")
    mock_get.side_effect = httpx.RequestError("Erro de conexão", request=request)

    service = CNPJService(repository=Mock())

    with pytest.raises(CNPJAPIError, match="Não foi possível conectar à API pública"):
        service.consultar("11222333000181")

def test_listar_historico_delega_para_repository():
    repository = Mock()
    repository.listar.return_value = ["consulta_1", "consulta_2"]

    service = CNPJService(repository=repository)

    resultado = service.listar_historico(limite=10)

    repository.listar.assert_called_once_with(limite=10)
    assert resultado == ["consulta_1", "consulta_2"]

def test_obter_estatisticas_delega_para_repository():
    repository = Mock()
    repository.estatisticas.return_value = {
        "total_consultas": 5,
        "total_favoritos": 2,
    }

    service = CNPJService(repository=repository)

    resultado = service.obter_estatisticas()

    repository.estatisticas.assert_called_once()
    assert resultado == {
        "total_consultas": 5,
        "total_favoritos": 2,
    }

def test_favoritar_retorna_payload_quando_cnpj_existe():
    repository = Mock()
    repository.favoritar.return_value = SimpleNamespace(
        id=1,
        cnpj="11222333000181",
        razao_social="EMPRESA TESTE LTDA",
    )

    service = CNPJService(repository=repository)

    resultado = service.favoritar("11222333000181")

    repository.favoritar.assert_called_once_with("11222333000181")
    assert resultado == {
        "mensagem": "CNPJ 11222333000181 favoritado com sucesso.",
        "consulta": {
            "id": 1,
            "cnpj": "11222333000181",
            "razao_social": "EMPRESA TESTE LTDA",
        },
    }

def test_favoritar_lanca_erro_quando_cnpj_nao_esta_no_historico():
    repository = Mock()
    repository.favoritar.return_value = None

    service = CNPJService(repository=repository)

    with pytest.raises(CNPJNotFoundError, match="não encontrado no histórico"):
        service.favoritar("11222333000181")

def test_desfavoritar_retorna_payload_quando_cnpj_existe():
    repository = Mock()
    repository.desfavoritar.return_value = SimpleNamespace(
        id=1,
        cnpj="11222333000181",
        razao_social="EMPRESA TESTE LTDA",
    )

    service = CNPJService(repository=repository)

    resultado = service.desfavoritar("11222333000181")

    repository.desfavoritar.assert_called_once_with("11222333000181")
    assert resultado == {
        "mensagem": "Favorito removido para o CNPJ 11222333000181."
    }

def test_desfavoritar_lanca_erro_quando_cnpj_nao_esta_favoritado():
    repository = Mock()
    repository.desfavoritar.return_value = None

    service = CNPJService(repository=repository)

    with pytest.raises(
        CNPJNotFoundError, 
        match="não está favoritado ou não encontrado"):
        service.desfavoritar("11222333000181")

def test_listar_favoritos_delega_para_repository():
    repository = Mock()
    repository.listar_favoritos.return_value = ["fav_1", "fav_2"]

    service = CNPJService(repository=repository)

    resultado = service.listar_favoritos(limite=5)

    repository.listar_favoritos.assert_called_once_with(limite=5)
    assert resultado == ["fav_1", "fav_2"]