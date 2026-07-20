from app.utils.cnpj import calcular_digito, limpar_cnpj, validar_cnpj


def test_limpar_cnpj_com_mascara() -> None:
    resultado = limpar_cnpj("41.364.174/0001-10")
    
    assert resultado == "41364174000110"


def test_calcular_primeiro_digito() -> None:
    resultado = calcular_digito(
        "413641740001",
        (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    )
    
    assert resultado == 1

def test_validar_cnpj_valido() -> None:
    assert validar_cnpj("41.364.174/0001-10")

def test_validar_cnpj_invalido() -> None:
    assert not validar_cnpj("41.364.174/0001-11")   

def test_validar_cnpj_invalido_com_tamanho_invalido() -> None:
    assert not validar_cnpj("41.364.174")  # 8 dígitos

def test_validar_cnpj_repetido() -> None:
    assert not validar_cnpj("11.111.111/1111-11")  # CNPJ repetido