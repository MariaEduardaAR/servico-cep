import io
import json
import unittest
from unittest.mock import call, patch
from urllib.error import HTTPError

from app.viacep import CepNaoEncontrado, FalhaViaCEP, consultar_cep


def erro_http(status):
    return HTTPError("https://viacep.com.br", status, "falha simulada", {}, None)


@patch("app.viacep.sleep")
@patch("app.viacep.urlopen")
class TestRetry(unittest.TestCase):
    def test_recupera_na_segunda_tentativa(self, abrir, pausa):
        endereco = {"cep": "01001-000", "bairro": "Sé", "logradouro": "Praça da Sé",
                    "localidade": "São Paulo", "uf": "SP"}
        abrir.side_effect = [erro_http(503), io.BytesIO(json.dumps(endereco).encode())]
        self.assertEqual(consultar_cep("01001-000")["cidade"], "São Paulo")
        self.assertEqual(abrir.call_count, 2)
        pausa.assert_called_once_with(0.2)

    def test_para_apos_tres_timeouts(self, abrir, pausa):
        abrir.side_effect = TimeoutError("demora simulada")
        with self.assertRaisesRegex(FalhaViaCEP, "3 tentativas"):
            consultar_cep("01001000")
        self.assertEqual(abrir.call_count, 3)
        self.assertEqual(pausa.call_args_list, [call(0.2), call(0.4)])

    def test_erro_http_permanente(self, abrir, pausa):
        abrir.side_effect = erro_http(403)
        with self.assertRaises(FalhaViaCEP):
            consultar_cep("01001000")
        abrir.assert_called_once()
        pausa.assert_not_called()

    def test_cep_inexistente(self, abrir, pausa):
        abrir.return_value = io.BytesIO(b'{"erro":"true"}')
        with self.assertRaises(CepNaoEncontrado):
            consultar_cep("99999999")
        abrir.assert_called_once()
        pausa.assert_not_called()

    def test_formato_invalido(self, abrir, pausa):
        with self.assertRaises(ValueError):
            consultar_cep("abc")
        abrir.assert_not_called()
        pausa.assert_not_called()
