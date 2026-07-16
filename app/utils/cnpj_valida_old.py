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

    if len(cnpj) != 14:
        return False

    if cnpj == cnpj[0] * 14:
        return False

    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]

    soma = sum(
        int(numero) * peso
        for numero, peso in zip(cnpj[:12], pesos1)
    )

    resto = soma % 11

    primeiro = 0 if resto < 2 else 11 - resto

    soma = sum(
        int(numero) * peso
        for numero, peso in zip(
            cnpj[:12] + str(primeiro),
            pesos2,
        )
    )

    resto = soma % 11

    segundo = 0 if resto < 2 else 11 - resto

    return cnpj[-2:] == f"{primeiro}{segundo}"