"""Consulta de endereço no ViaCEP."""
import json
import logging
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from app.cep import normalizar_cep


class CepNaoEncontrado(LookupError):
    pass


class FalhaViaCEP(RuntimeError):
    pass


def consultar_cep(cep: str) -> dict[str, str]:
    numero = normalizar_cep(cep)
    url = f"https://viacep.com.br/ws/{numero}/json/"
    dados = _ler_com_retry(url)

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


def _ler_com_retry(url: str):
    """Faz até três tentativas, com pausas de 0,2 e 0,4 segundo."""
    for tentativa in range(1, 4):
        try:
            with urlopen(url, timeout=5) as resposta:
                return json.load(resposta)
        except HTTPError as erro:
            erro.close()
            if erro.code not in {408, 500, 502, 503, 504}:
                raise FalhaViaCEP(f"O ViaCEP respondeu com HTTP {erro.code}.") from erro
            causa = erro
        except (URLError, TimeoutError, ConnectionError) as erro:
            causa = erro
        except OSError as erro:
            raise FalhaViaCEP("Falha ao consultar o ViaCEP.") from erro
        except ValueError as erro:
            raise FalhaViaCEP("O ViaCEP enviou uma resposta inválida.") from erro

        logging.getLogger(__name__).warning("ViaCEP: tentativa %d/3 falhou.", tentativa)
        if tentativa == 3:
            raise FalhaViaCEP("ViaCEP indisponível após 3 tentativas.") from causa
        sleep(0.2 * tentativa)
