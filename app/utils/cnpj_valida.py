def limpar_cnpj(cnpj: str) -> str:
    """
    Limpa o CNPJ removendo caracteres não numéricos.

    Args:
        cnpj (str): O CNPJ a ser limpo.
        Ex.: '12.345.678/0001-90'

    Returns:
        str: O CNPJ limpo, contendo apenas números.
    Ex.: '12345678000190'
    """
    return ''.join(
        caractere 
        for caractere 
        in cnpj if caractere.isdigit()
    )

def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ.

    Args:
        cnpj (str): O CNPJ a ser validado.
        Ex.: '12.345.678/0001-90'

    Returns:
        bool: True se o CNPJ for válido, False caso contrário.
    """
    cnpj = limpar_cnpj(cnpj)

    if len(cnpj) != 14 or cnpj in (c * 14 for c in "1234567890"):
        return False

    def calcular_digito(cnpj: str, peso: list) -> int:
        soma = sum(
            int(digito) * peso[i] 
            for i, digito in enumerate(cnpj)
        )
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [6] + peso1[:-1]

    digito1 = calcular_digito(cnpj[:12], peso1)
    digito2 = calcular_digito(cnpj[:12] + str(digito1), peso2)

    return cnpj[-2:] == f"{digito1}{digito2}"