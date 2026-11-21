"""Consulta de endereço no ViaCEP."""
import json
from urllib.error import URLError
from urllib.request import urlopen

from app.cep import normalizar_cep


class CepNaoEncontrado(LookupError):
    pass


class FalhaViaCEP(RuntimeError):
    pass


def consultar_cep(cep: str) -> dict[str, str]:
    numero = normalizar_cep(cep)
    url = f"https://viacep.com.br/ws/{numero}/json/"
    try:
        with urlopen(url, timeout=5) as resposta:
            dados = json.load(resposta)
    except (URLError, OSError) as erro:
        raise FalhaViaCEP("Falha de conexão com o ViaCEP.") from erro
    except ValueError as erro:
        raise FalhaViaCEP("O ViaCEP enviou uma resposta inválida.") from erro

    if isinstance(dados, dict) and dados.get("erro") in (True, "true"):
        raise CepNaoEncontrado("CEP não encontrado.")

    campos = ("cep", "logradouro", "bairro", "localidade", "uf")
    if not isinstance(dados, dict) or not all(isinstance(dados.get(c), str) for c in campos):
        raise FalhaViaCEP("O ViaCEP enviou um endereço em formato inesperado.")
    return {
        "cep": dados["cep"],
        "logradouro": dados["logradouro"],
        "bairro": dados["bairro"],
        "cidade": dados["localidade"],
        "uf": dados["uf"],
    }
