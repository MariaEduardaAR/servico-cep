import io
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError

from fastapi.testclient import TestClient
from app.main import app


@patch("app.viacep.urlopen")
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.cliente = TestClient(app)
        self.addCleanup(self.cliente.close)

    def test_sucesso(self, abrir):
        endereco = {"cep": "01001-000", "logradouro": "Praça da Sé",
                    "bairro": "Sé", "localidade": "São Paulo", "uf": "SP"}
        abrir.return_value = io.BytesIO(json.dumps(endereco).encode())
        resposta = self.cliente.get("/ceps/01001-000")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["cidade"], "São Paulo")

    def test_invalido(self, abrir):
        self.assertEqual(self.cliente.get("/ceps/abc").status_code, 400)
        abrir.assert_not_called()

    def test_inexistente(self, abrir):
        abrir.return_value = io.BytesIO(b'{"erro": "true"}')
        self.assertEqual(self.cliente.get("/ceps/99999999").status_code, 404)

    def test_provedor_indisponivel(self, abrir):
        abrir.side_effect = URLError("sem rede")
        self.assertEqual(self.cliente.get("/ceps/01001000").status_code, 502)
