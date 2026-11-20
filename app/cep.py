import re


def normalizar_cep(cep: str) -> str:
    """Valida o formato do CEP e devolve os oito dígitos."""
    if not re.fullmatch(r"[0-9]{5}-?[0-9]{3}", cep):
        raise ValueError("CEP inválido. Use 01001000 ou 01001-000.")

    return cep.replace("-", "")
