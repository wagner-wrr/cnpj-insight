def limpar_cnpj(cnpj: str) -> str:
    """
    Remove caracteres não numéricos de um CNPJ.
    """
    return ''.join(
        caractere 
        for caractere in cnpj 
        if caractere.isdigit()
    )

def calcular_digito(
        numero: str,
        pesos: tuple[int, ...],
) -> int:
    """Calcula o dígito verificador de um CNPJ."""

    soma = sum(
        int(digito) * peso 
        for digito, peso in zip(numero, pesos)
    )

    resto = soma % 11

    if resto < 2:
        return 0
    
    return 11 - resto

def validar_cnpj(cnpj: str) -> bool:
    """Valida um CNPJ pelos dígitos verificadores."""
    cnpj = limpar_cnpj(cnpj)

    if len(cnpj) != 14:
        return False
    
    if cnpj == cnpj[0] * 14:
        return False

    primeiro = calcular_digito(
        cnpj[:12],
        (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    )

    segundo = calcular_digito(
        cnpj[:12] + str(primeiro),
        (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    )

    return cnpj[-2:] == f"{primeiro}{segundo}"