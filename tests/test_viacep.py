import io
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError

from app.viacep import CepNaoEncontrado, FalhaViaCEP, consultar_cep


@patch("app.viacep.urlopen")
class TestViaCEP(unittest.TestCase):
    def test_endereco(self, abrir):
        dados = {"cep": "01001-000", "logradouro": "Praça da Sé", "bairro": "Sé",
                 "localidade": "São Paulo", "uf": "SP"}
        abrir.return_value = io.BytesIO(json.dumps(dados).encode())
        endereco = consultar_cep("01001-000")
        self.assertEqual(endereco["cidade"], "São Paulo")
        self.assertEqual(endereco["cep"], "01001-000")
        abrir.assert_called_once_with("https://viacep.com.br/ws/01001000/json/", timeout=5)

    def test_formato_invalido(self, abrir):
        with self.assertRaises(ValueError):
            consultar_cep("12ABC")
        abrir.assert_not_called()

    def test_inexistente(self, abrir):
        abrir.return_value = io.BytesIO(b'{"erro":"true"}')
        with self.assertRaises(CepNaoEncontrado):
            consultar_cep("99999999")

    def test_falha_conexao(self, abrir):
        abrir.side_effect = URLError("sem rede")
        with self.assertRaises(FalhaViaCEP):
            consultar_cep("01001000")

    def test_json_invalido(self, abrir):
        abrir.return_value = io.BytesIO(b"indisponivel")
        with self.assertRaises(FalhaViaCEP):
            consultar_cep("01001000")

    def test_dados_incompletos(self, abrir):
        abrir.return_value = io.BytesIO(b"{}")
        with self.assertRaises(FalhaViaCEP):
            consultar_cep("01001000")
