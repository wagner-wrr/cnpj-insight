from app.utils.cnpj_valida import limpar_cnpj


def test_limpar_cnpj():
    assert (
        limpar_cnpj(
            "41.364.174/0001-10"
        ) 
        == "41364174000110"
    )