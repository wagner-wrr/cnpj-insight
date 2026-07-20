from app.models.consulta import Consulta
from app.repositories.consulta_repository import ConsultaRepository
from app.routers.cnpj import favoritar

def test_salvar_persiste_consulta(session_test):
    repository = ConsultaRepository(session_test)

    consulta = Consulta(
        cnpj = "11222333000181",
        razao_social = "EMPRESA TESTE LTDA",    
        nome_fantasia= "EMPRESA TESTE",
        situacao = "ATIVA",
        cidade = "Eunápolis",
        uf = "BA",
    )

    salva = repository.salvar(consulta)

    assert salva.id is not None
    assert salva.cnpj == "11222333000181"
    assert salva.razao_social == "EMPRESA TESTE LTDA"

def test_listar_retorna_consultas(session_test):
    repository = ConsultaRepository(session_test)

    repository.salvar(
        Consulta(
            cnpj = "11222333000181",
            razao_social = "EMPRESA A",    
            nome_fantasia= "A",
            situacao = "ATIVA",
            cidade = "Eunápolis",
            uf = "BA",
        )
    )

    repository.salvar(
        Consulta(
            cnpj = "22333444000199",
            razao_social = "EMPRESA B",    
            nome_fantasia= "B",
            situacao = "ATIVA",
            cidade = "Eunápolis",
            uf = "BA",
        )
    )

    resultado = repository.listar(limite=10)

    assert len(resultado) == 2
    cnpjs = [item.cnpj for item in resultado]
    assert "11222333000181" in cnpjs
    assert "22333444000199" in cnpjs

def test_estatisticas_retorna_totais(session_test):
    repository = ConsultaRepository(session_test)

    repository.salvar(
        Consulta(
            cnpj="11222333000181",
            razao_social="EMPRESA A",
            nome_fantasia="A",
            situacao="ATIVA",
            cidade="Eunápolis",
            uf="BA",
            favorito=False,
        )
    )

    repository.salvar(
        Consulta(
            cnpj="22333444000199",
            razao_social="EMPRESA B",
            nome_fantasia="B",
            situacao="ATIVA",
            cidade="Serra",
            uf="ES",
            favorito=True,
        )
    )

    estatisticas = repository.estatisticas()

    assert estatisticas["total_consultas"] == 2
    assert estatisticas["total_favoritos"] == 1

def test_favoritar_marca_consulta_como_favorita(session_test):
    repository = ConsultaRepository(session_test)

    repository.salvar(
        Consulta(
            cnpj="11222333000181",
            razao_social="EMPRESA TESTE LTDA",
            nome_fantasia="EMPRESA TESTE",
            situacao="ATIVA",
            cidade="Eunápolis",
            uf="BA",
            favorito=False,
        )
    )

    resultado = repository.favoritar("11222333000181")

    assert resultado is not None
    assert resultado.favorito is True

def test_favoritar_retorna_none_quando_cnpj_nao_existe(session_test):
    repository = ConsultaRepository(session_test)

    resultado = repository.favoritar("00000000000000")

    assert resultado is None

def test_desfavoritar_remove_favorito(session_test):
    repository = ConsultaRepository(session_test)

    repository.salvar(
        Consulta(
            cnpj="11222333000181",
            razao_social="EMPRESA TESTE LTDA",
            nome_fantasia="EMPRESA TESTE",
            situacao="ATIVA",
            cidade="Eunápolis",
            uf="BA",
            favorito=True,
        )
    )

    resultado = repository.desfavoritar("11222333000181")

    assert resultado is not None
    assert resultado.favorito is False

def test_desfavoritar_retorna_none_quando_cnpj_nao_existe(session_test):
    repository = ConsultaRepository(session_test)

    resultado = repository.desfavoritar("00000000000000")

    assert resultado is None

def test_listar_favoritos_retorna_apenas_favoritados(session_test):
    repository = ConsultaRepository(session_test)

    repository.salvar(
        Consulta(
            cnpj="11222333000181",
            razao_social="EMPRESA A",
            nome_fantasia="A",
            situacao="ATIVA",
            cidade="Eunápolis",
            uf="BA",
            favorito=True,
        )
    )

    repository.salvar(
        Consulta(
            cnpj="22333444000199",
            razao_social="EMPRESA B",
            nome_fantasia="B",
            situacao="ATIVA",
            cidade="Eunápolis",
            uf="BA",
            favorito=False,
        )
    )

    favoritos = repository.listar_favoritos(limite=10)

    assert len(favoritos) == 1
    assert favoritos[0].cnpj == "11222333000181"
    assert favoritos[0].favorito is True